import logging
import os
import xml.etree.ElementTree as ET

from FileManager import get_test_coverage_dir, join_path, SPECTRUM_PASSED_COVERAGE_FILE_NAME, get_variants_dir, \
    list_dir, get_all_coverage_file_paths_in_dir


# __START__ Author: tuanngokien

def find_optimal_test_cases_with_target_coverage(failed_test_coverage_dir, passed_test_coverage_dir,
                                                 target_coverage=0.5):
    """
    loading coverage items (see function "get_all_coverage_flag_items" for more detail)
    locate failed coverage in the first place for exploring satisfied subset more quickly
    """
    # failed_coverage_file_paths = get_all_coverage_file_paths_in_dir(
    #     failed_test_coverage_dir) if failed_test_coverage_dir else []
    # failed_coverage_flags = get_statement_coverage_flags(failed_coverage_file_paths)
    # print("__FAILED__", "[{}] [{}] {}".format(
    #     get_statement_coverage_from_flags(failed_coverage_flags) if failed_coverage_flags else "N/A",
    #     len(failed_coverage_file_paths),
    #     get_all_test_coverage_by_result_dir(failed_test_coverage_dir) if failed_test_coverage_dir else []))
    #
    # passed_coverage_file_paths = get_all_coverage_file_paths_in_dir(passed_test_coverage_dir)
    # passed_coverage_flags = get_statement_coverage_flags(passed_coverage_file_paths)
    # print("__PASSED__", "[{}] [{}] {}".format(get_statement_coverage_from_flags(passed_coverage_flags),
    #                                           len(passed_coverage_file_paths),
    #                                           get_all_test_coverage_by_result_dir(passed_test_coverage_dir)))
    #
    # merged_coverage_flags = merge_coverage_flags(passed_coverage_flags, failed_coverage_flags)
    # print("___ALL____", "[{}] [{}]".format(get_statement_coverage_from_flags(merged_coverage_flags), len(failed_coverage_file_paths) + len(passed_coverage_file_paths)),)
    # return

    failed_coverage_items = get_all_coverage_flag_items(failed_test_coverage_dir)
    passed_coverage_items = get_all_coverage_flag_items(passed_test_coverage_dir)
    if failed_coverage_items:
        remaining_coverage_items = failed_coverage_items[1:] + passed_coverage_items
        # shuffle(remaining_coverage_items)
        remaining_coverage_items.sort(reverse=True)
        single_coverage_items = [failed_coverage_items[0]] + remaining_coverage_items
    else:
        single_coverage_items = passed_coverage_items
    single_coverage_items = list(filter(lambda item: item[0] <= target_coverage, single_coverage_items))

    """
    merge coverage items to meet required coverage
    using dynamic programming 
    https://stackoverflow.com/questions/16022205/how-do-i-find-the-closest-possible-sum-of-an-arrays-elements-to-a-particular-va
    zero_coverage_item is variable "opt" in related link
    """
    zero_coverage_item = (0.0, [False] * len(single_coverage_items[0][1]), [])
    merged_coverage_items = [zero_coverage_item]
    optimal_coverage_delta = target_coverage
    for single_item in single_coverage_items:
        sub_merged_coverage_items = []
        for merged_item in merged_coverage_items:
            new_merged_item = merge_coverage_items(merged_item, single_item)
            new_coverage_value = new_merged_item[0]
            new_coverage_delta = abs(new_coverage_value - target_coverage)
            if new_coverage_delta > 0.01:
                if new_coverage_delta < optimal_coverage_delta:
                    print(new_coverage_value)
                    optimal_coverage_delta = new_coverage_delta
                else:
                    print("Finding {} ...".format(len(merged_coverage_items)), end='\r')
                sub_merged_coverage_items.append(new_merged_item)
            else:
                print(new_merged_item)
                return new_merged_item
        merged_coverage_items.extend(sub_merged_coverage_items)


def merge_coverage_items(first_item, second_item):
    new_flags = merge_coverage_flags(first_item[1], second_item[1])
    new_coverage_value = get_statement_coverage_from_flags(new_flags)
    new_coverage_source_files = first_item[2] + second_item[2]
    return new_coverage_value, new_flags, new_coverage_source_files


def get_all_coverage_flag_items(coverage_dir):
    if not coverage_dir:
        return []
    coverage_file_paths = get_all_coverage_file_paths_in_dir(coverage_dir)

    """
    each item is formatted as (coverage_value, coverage_flags, file_path).
    eg, (0.56, [False, True, False], ["/root/coverage/passed/ElevatorSystem.Floor_ESTest.test8.coverage.xml"])
    """

    coverage_item_containers = []
    duplicated_test_flags = []
    for file_path in coverage_file_paths:
        current_coverage_flags = get_statement_coverage_flags([file_path, ])
        if current_coverage_flags in duplicated_test_flags:
            continue
        else:
            duplicated_test_flags.append(current_coverage_flags)
        current_coverage_value = get_statement_coverage_from_flags(current_coverage_flags)
        if current_coverage_value > 0:
            coverage_item_containers.append((current_coverage_value, current_coverage_flags, []))
    return sorted(coverage_item_containers)


def get_all_test_coverage_by_result_dir(test_coverage_dir, unique=False, sort=False):
    coverage_file_paths = get_all_coverage_file_paths_in_dir(test_coverage_dir)
    failed_coverages = []
    for coverage_file_path in coverage_file_paths:
        current_test_coverage = get_statement_coverage([coverage_file_path], rounded=True)
        if current_test_coverage > 0:
            failed_coverages.append(current_test_coverage)
    if unique:
        failed_coverages = list(set(failed_coverages))
    if sort:
        failed_coverages.sort()
    return failed_coverages


def get_statement_coverage(coverage_file_paths, rounded=False):
    stm_coverage_flags = get_statement_coverage_flags(coverage_file_paths)
    return get_statement_coverage_from_flags(stm_coverage_flags, rounded)


def merge_coverage_flags(first_flags, second_flags):
    if not first_flags:
        raise Exception("first_flags must be a not-null coverage vector")
    elif not second_flags:
        second_flags = [False] * len(first_flags)
    return [f or s for f, s in zip(first_flags, second_flags)]


def get_statement_coverage_from_flags(stm_coverage_flags, rounded=False):
    stm_coverage = sum(stm_coverage_flags) / len(stm_coverage_flags)
    if rounded:
        stm_coverage = round(stm_coverage, 3)
    return stm_coverage


def get_statement_coverage_flags(coverage_file_paths):
    stm_coverage_flags = []
    for coverage_file_path in coverage_file_paths:
        tree = ET.parse(coverage_file_path)
        root = tree.getroot()
        line_elms = root.findall(".//line[@count]")
        if len(stm_coverage_flags) == 0:
            stm_coverage_flags = [False] * len(line_elms)
        elif len(stm_coverage_flags) != len(line_elms):
            raise Exception("Inconsistent coverage lines between files {}".format(coverage_file_paths))
        for i, elm in enumerate(line_elms):
            if int(elm.get("count")) > 0 and stm_coverage_flags[i] == False:
                stm_coverage_flags[i] = True
    return stm_coverage_flags


# __END__

def statement_coverage(variant_dir, spectrum_coverage_prefix):
    global NEW_SPECTRUM_PASSED_COVERAGE_FILE_NAME
    NEW_SPECTRUM_PASSED_COVERAGE_FILE_NAME = spectrum_coverage_prefix + SPECTRUM_PASSED_COVERAGE_FILE_NAME

    test_coverage_dir = get_test_coverage_dir(variant_dir)
    spectrum_passed_coverage_file = join_path(test_coverage_dir, NEW_SPECTRUM_PASSED_COVERAGE_FILE_NAME)
    if not os.path.isfile(spectrum_passed_coverage_file):
        spectrum_passed_coverage_file = join_path(test_coverage_dir, SPECTRUM_PASSED_COVERAGE_FILE_NAME)
    num_of_stm = 0
    untested_stm = 0
    if os.path.isfile(spectrum_passed_coverage_file):
        try:
            tree = ET.parse(spectrum_passed_coverage_file)
            root = tree.getroot()
            project = root.find("project")
            for package in project:
                for file in package:
                    for line in file:
                        num_of_stm += 1
                        if (int(line.get("count")) == 0):
                            untested_stm += 1
        except:
            logging.info("Exception when parsing %s", spectrum_passed_coverage_file)
    else:
        logging.info("spectrum passed coveraged file does not exist in %s", variant_dir)

    coverage_rate = (num_of_stm - untested_stm) / num_of_stm
    return coverage_rate


def statement_coverage_of_variants(project_dir, spectrum_coverage_prefix=""):
    stm_coverage_variants = {}
    variants_dir = get_variants_dir(project_dir)
    for variant in list_dir(variants_dir):
        variant_dir = join_path(variants_dir, variant)
        testing_coverage = statement_coverage(variant_dir, spectrum_coverage_prefix)
        stm_coverage_variants[variant] = testing_coverage
    return stm_coverage_variants

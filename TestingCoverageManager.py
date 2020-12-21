import logging
import os
import xml.etree.ElementTree as ET

from FileManager import get_test_coverage_dir, join_path, SPECTRUM_PASSED_COVERAGE_FILE_NAME, get_variants_dir, \
    list_dir, get_all_coverage_file_paths_in_dir


# __________START__________ Author: tuanngokien

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

    failed_coverage_items, failed_coverage_file_path_mapping = get_all_coverage_flag_items(failed_test_coverage_dir,
                                                                                           file_mapping_prefix="f")
    passed_coverage_items, passed_coverage_file_path_mapping = get_all_coverage_flag_items(passed_test_coverage_dir,
                                                                                           file_mapping_prefix="p")
    coverage_file_path_mapping = {**failed_coverage_file_path_mapping, **passed_coverage_file_path_mapping}
    if failed_coverage_items:
        remaining_coverage_items = failed_coverage_items[1:] + passed_coverage_items
        # shuffle(remaining_coverage_items)
        remaining_coverage_items.sort(reverse=True)
        single_coverage_items = [failed_coverage_items[0]] + remaining_coverage_items
    else:
        single_coverage_items = [passed_coverage_items[0]] + sorted(passed_coverage_items[1:], reverse=True)
    full_coverage_item = merge_coverage_items(*single_coverage_items)
    print("[Full coverage]", full_coverage_item[0])
    if full_coverage_item[0] < target_coverage:
        raise Exception(f"Raw test suite coverage can not satisfy required value {target_coverage}")

    single_coverage_items = [single_coverage_items[0]] + list(
        filter(lambda item: item[0] <= target_coverage, single_coverage_items[1:]))
    # find solution
    merged_item = find_merged_coverage_item_with_target_coverage(single_coverage_items, target_coverage,
                                                                 shallow_mode=True)
    if not merged_item:
        print("%%%%%%% Try to use deep mode to find solution %%%%%%%")
        merged_item = find_merged_coverage_item_with_target_coverage(single_coverage_items, target_coverage,
                                                                     shallow_mode=False)
    if merged_item:
        print(f"------- FOUND A SOLUTION [{merged_item[0]}] ------")
        build_spectrum_coverage_from_merged_item(merged_item, coverage_file_path_mapping)
    else:
        print("******* NO SOLUTION ********")
        input("Press Enter to continue...")


def build_spectrum_coverage_from_merged_item(merge_item, coverage_file_path_mapping):
    coverage_value = merge_item[0]
    file_ids = merge_item[2]
    for file_id in file_ids:
        print(coverage_file_path_mapping[file_id])


def find_merged_coverage_item_with_target_coverage(single_coverage_items, target_coverage, shallow_mode=True):
    """
    merge coverage items to meet required coverage
    using dynamic programming algorithm
    https://stackoverflow.com/questions/16022205/how-do-i-find-the-closest-possible-sum-of-an-arrays-elements-to-a-particular-va
    zero_coverage_item is the variable "opt" in related link, it also has the same dimension as other coverage vectors
    """

    zero_coverage_item = (0.0, [False] * len(single_coverage_items[0][1]), [])
    merged_coverage_items = [zero_coverage_item]
    optimal_coverage_delta = target_coverage
    for single_item in single_coverage_items:
        sub_merged_coverage_items = []
        for merged_item in merged_coverage_items[::-1]:
            new_merged_item = merge_coverage_items(merged_item, single_item)
            new_coverage_value = new_merged_item[0]
            if new_coverage_value <= merged_item[0]:
                continue
            if shallow_mode:
                should_continue = False
                for added_item in sub_merged_coverage_items:
                    temp_item = merge_coverage_items(added_item, new_merged_item)
                    if temp_item[0] <= added_item[0]:
                        should_continue = True
                        break
                if should_continue:
                    continue

            new_coverage_delta = abs(new_coverage_value - target_coverage)
            if new_coverage_delta < optimal_coverage_delta:
                print(f"{new_coverage_value} [{len(merged_coverage_items)}]")
                optimal_coverage_delta = new_coverage_delta
            if new_coverage_delta > 0.01:
                print("Finding {} ...".format(len(merged_coverage_items)), end='\r')
                sub_merged_coverage_items.append(new_merged_item)
            else:
                # print(new_merged_item)
                return new_merged_item
        merged_coverage_items.extend(sub_merged_coverage_items)


def merge_coverage_items(*args):
    new_flags = merge_coverage_flags(*[item[1] for item in args])
    new_coverage_value = get_statement_coverage_from_flags(new_flags)
    new_coverage_source_files = [file_id for item in args for file_id in item[2]]
    return new_coverage_value, new_flags, new_coverage_source_files


def get_all_coverage_flag_items(coverage_dir, file_mapping_prefix="a"):
    """
    each item is formatted as (coverage_value, coverage_flags, file_path).
    eg, (0.56, [False, True, False], ["/root/coverage/passed/ElevatorSystem.Floor_ESTest.test8.coverage.xml"])
    """
    if not coverage_dir:
        return []
    coverage_file_paths = get_all_coverage_file_paths_in_dir(coverage_dir)

    coverage_item_containers = []
    coverage_file_path_mapping = {}
    duplicated_test_flags = []
    for i, file_path in enumerate(coverage_file_paths):
        current_coverage_flags = get_statement_coverage_flags([file_path, ])
        if current_coverage_flags in duplicated_test_flags:
            continue
        else:
            duplicated_test_flags.append(current_coverage_flags)
        current_coverage_value = get_statement_coverage_from_flags(current_coverage_flags)
        if current_coverage_value > 0:
            file_id = f"{file_mapping_prefix}{i}"
            coverage_file_path_mapping[file_id] = file_path
            coverage_item_containers.append((current_coverage_value, current_coverage_flags, [file_id, ]))
    return sorted(coverage_item_containers), coverage_file_path_mapping


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


def merge_coverage_flags(*args):
    flags_container = list(args)
    if len(flags_container) <= 1:
        raise Exception("Passing at least 2 flags to merge")
    first_flags = flags_container[0]
    if not first_flags:
        raise Exception("first_flags must be a not-null coverage vector")
    for i, flags in enumerate(flags_container):
        if not flags:
            flags_container[i] = [False] * len(first_flags)
    return [any(item) for item in zip(*flags_container)]


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
        if len(stm_coverage_flags) <= 0:
            stm_coverage_flags = [False] * len(line_elms)
        elif len(stm_coverage_flags) != len(line_elms):
            raise Exception("Inconsistent coverage lines between files {}".format(coverage_file_paths))
        for i, elm in enumerate(line_elms):
            if int(elm.get("count")) > 0 and stm_coverage_flags[i] == False:
                stm_coverage_flags[i] = True
    return stm_coverage_flags


# __________END__________

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

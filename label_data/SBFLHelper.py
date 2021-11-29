import logging
import os
import xml.etree.ElementTree as ET

from FileManager import get_all_variant_dirs, get_test_coverage_dir, \
    get_spectrum_failed_coverage_file_name_with_version, join_path, get_spectrum_passed_coverage_file_name_with_version, \
    get_variants_dir, list_dir, get_variant_dir, SPECTRUM_FAILED_COVERAGE_FILE_NAME, SPECTRUM_PASSED_COVERAGE_FILE_NAME, \
    get_failed_test_coverage_dir, get_passed_test_coverage_dir
from TestingCoverageManager import statement_coverage
from label_data.SpectrumReader import read_coverage_file
from ranking.Keywords import FAILED_TEST_COUNT, PASSED_TEST_COUNT
from ranking.RankingManager import read_coverage_info_for_spectrum, count_tests


def get_infor_for_sbfl_consistent_testing_version(mutated_project_dir, failing_variants, spectrum_coverage_prefix,
                                                  coverage_rate):
    total_failed_tests = 0
    total_passed_tests = 0
    stm_info_for_spectrum = {}
    variants_list = get_all_variant_dirs(mutated_project_dir)
    for variant_dir in variants_list:
        stm_coverage = 0
        if coverage_rate > 0:
            stm_coverage = statement_coverage(variant_dir, spectrum_coverage_prefix)
        test_coverage_dir = get_test_coverage_dir(variant_dir)
        spectrum_failed_file = get_spectrum_failed_coverage_file_name_with_version(spectrum_coverage_prefix)
        spectrum_failed_coverage_file_dir = join_path(test_coverage_dir, spectrum_failed_file)
        spectrum_passed_file = get_spectrum_passed_coverage_file_name_with_version(spectrum_coverage_prefix)
        spectrum_passed_coverage_file_dir = join_path(test_coverage_dir, spectrum_passed_file)

        # if variant is a passing variant and stm_coverage < coverage_rate
        if not os.path.isfile(
                spectrum_failed_coverage_file_dir) and coverage_rate != 0 and stm_coverage <= coverage_rate:
            continue
        if variant_dir.split("/")[-1] in failing_variants and os.path.isfile(spectrum_failed_coverage_file_dir):
            stm_info_for_spectrum = read_coverage_info_for_spectrum(stm_info_for_spectrum,
                                                                    spectrum_failed_coverage_file_dir,
                                                                    FAILED_TEST_COUNT)

        if os.path.isfile(spectrum_passed_coverage_file_dir):
            stm_info_for_spectrum = read_coverage_info_for_spectrum(stm_info_for_spectrum,
                                                                    spectrum_passed_coverage_file_dir,
                                                                    PASSED_TEST_COUNT)

        ftests, ptests = count_tests(test_coverage_dir, spectrum_coverage_prefix)
        if variant_dir.split("/")[-1] in failing_variants:
            total_failed_tests += ftests
        total_passed_tests += ptests

    return stm_info_for_spectrum, total_passed_tests, total_failed_tests


def get_passing_executions(project_dir, system_stm_ids, variants):
    passed_test_executions = {}
    for variant in variants:
        passed_test_executions[variant] = {}
        variant_dir = get_variant_dir(project_dir, variant)
        passed_tests_coverage_dir = get_passed_test_coverage_dir(variant_dir)
        all_passed_spectrums = list_dir(passed_tests_coverage_dir)
        for file in all_passed_spectrums:
            file_dir = join_path(passed_tests_coverage_dir, file)
            passed_test_executions[variant][file] = read_coverage_file(system_stm_ids[variant], file_dir)
    return passed_test_executions


def get_passing_executions_in_a_variant(project_dir, system_stm_ids, variant):
    passed_test_executions = {}
    variant_dir = get_variant_dir(project_dir, variant)
    passed_tests_coverage_dir = get_passed_test_coverage_dir(variant_dir)
    all_passed_spectrums = list_dir(passed_tests_coverage_dir)
    for file in all_passed_spectrums:
        file_dir = join_path(passed_tests_coverage_dir, file)
        passed_test_executions[file] = read_coverage_file(system_stm_ids[variant], file_dir)
    return passed_test_executions


def get_suspicious_space_consistent_version(mutated_project_dir, failing_variants, filtering_coverage_rate,
                                            coverage_version):
    all_stms_of_the_system, all_stms_in_failing_products = get_executed_stms_of_the_system_consistent_testing_version(
        mutated_project_dir, failing_variants, coverage_version, filtering_coverage_rate)

    return all_stms_in_failing_products


def get_executed_stms_of_the_system_consistent_testing_version(mutated_project_dir, failing_variants,
                                                               spectrum_coverage_prefix, coverage_rate):
    variants_dir = get_variants_dir(mutated_project_dir)
    variants_list = list_dir(variants_dir)
    all_stms_in_system = {}
    all_stms_in_failing_product = {}
    for variant in variants_list:
        stm_coverage = 0
        variant_dir = get_variant_dir(mutated_project_dir, variant)
        test_coverage_dir = get_test_coverage_dir(variant_dir)
        if coverage_rate > 0:
            stm_coverage = statement_coverage(variant_dir, spectrum_coverage_prefix)
        spectrum_failed_file = get_spectrum_failed_coverage_file_name_with_version(spectrum_coverage_prefix)
        if variant in failing_variants:
            failed_file = join_path(test_coverage_dir, spectrum_failed_file)
        else:
            failed_file = ""
        spectrum_passed_file = get_spectrum_passed_coverage_file_name_with_version(spectrum_coverage_prefix)
        passed_file = join_path(test_coverage_dir, spectrum_passed_file)

        # if variant is a passing coverage and statement coverage is less than the coverage rate
        if not os.path.isfile(failed_file) and coverage_rate != 0 and stm_coverage <= coverage_rate:
            continue

        coverage_files = [failed_file, passed_file]

        for c_file in coverage_files:
            if os.path.isfile(c_file):
                data = {}
                try:
                    tree = ET.parse(c_file)
                    root = tree.getroot()
                    project = root.find("project")

                    for package in project:
                        for file in package:
                            for line in file:
                                id = line.get('featureClass') + "." + line.get('featureLineNum')
                                if id not in data:
                                    data[id] = {'num_interactions': 0}
                except:
                    logging.info("Exception when parsing %s", c_file)
                all_stms_in_system[variant] = data
                if coverage_files.index(c_file) == 0:
                    all_stms_in_failing_product[variant] = data
    return all_stms_in_system, all_stms_in_failing_product

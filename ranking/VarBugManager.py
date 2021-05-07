import os

from FileManager import get_variants_dir, list_dir, get_variant_dir, get_test_coverage_dir, join_path, \
    get_spectrum_failed_coverage_file_name_with_version
from TestingCoverageManager import statement_coverage


def is_var_bug(mutated_project_dir, filter_coverage, spectrum_coverage_prefix=""):
    num_of_failing_variants = 0
    num_of_passing_variants = 0
    variants_dir = get_variants_dir(mutated_project_dir)
    variants_list = list_dir(variants_dir)
    for variant in variants_list:
        variant_dir = get_variant_dir(mutated_project_dir, variant)
        test_coverage_dir = get_test_coverage_dir(variant_dir)
        stm_coverage = statement_coverage(variant_dir, spectrum_coverage_prefix)
        spectrum_failed_file = get_spectrum_failed_coverage_file_name_with_version(spectrum_coverage_prefix)
        failed_file = join_path(test_coverage_dir, spectrum_failed_file)
        if os.path.isfile(failed_file):
            num_of_failing_variants += 1
        elif stm_coverage >= filter_coverage:
            num_of_passing_variants += 1
        # if not os.path.isfile(failed_file):
        #     print(variant)
        #     print(stm_coverage)

    if (num_of_failing_variants >= 1 and num_of_passing_variants >= 1):
        return 1
    return 0

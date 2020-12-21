import sys

import TestingCoverageManager
from FileManager import list_dir, get_all_variant_dirs, get_passed_test_coverage_dir, get_failed_test_coverage_dir

if __name__ == "__main__":
    # sys.stdout = open("email_test_coverage.txt", "w")
    base_dir = "/Users/tuanngokien/Desktop/Software_Analysis/configurable_system/dataset/4wise-Email-FH-JML"
    mutated_project_dirs = list_dir(base_dir, full_path=True, sort=True)
    for mutated_project_dir in mutated_project_dirs[:1]:
        mutated_variant_dirs = get_all_variant_dirs(mutated_project_dir, sort=True)
        for mutated_variant_dir in mutated_variant_dirs[:]:
            if True or "model_m_ca4_0003" in mutated_variant_dir:
                print("-" * 20)
                print(mutated_variant_dir)
                failed_test_coverage_dir = get_failed_test_coverage_dir(mutated_variant_dir)
                passed_test_coverage_dir = get_passed_test_coverage_dir(mutated_variant_dir)
                TestingCoverageManager.find_optimal_test_cases_with_target_coverage(failed_test_coverage_dir, passed_test_coverage_dir)
    # sys.stdout.close()

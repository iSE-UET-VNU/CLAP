import sys

import SpectrumCoverageManager
import TestingCoverageManager
from FileManager import list_dir, get_all_variant_dirs, get_passed_test_coverage_dir, get_failed_test_coverage_dir, \
    get_test_coverage_dir
from SpectrumCoverageManager import rebuild_failed_spectrum_coverage_from_specific_test_cases, \
    rebuild_passed_spectrum_coverage_from_specific_test_cases

if __name__ == "__main__":
    # ------ START CONFIG ------
    base_dir = "/Users/tuanngokien/Desktop/Software_Analysis/configurable_system/dataset/4wise-Email-FH-JML"
    target_coverage = 0.4
    # ------ END CONFIG ------

    mutated_project_dirs = list_dir(base_dir, full_path=True, sort=True)
    for mutated_project_dir in mutated_project_dirs[:]:
        if "_MultipleBugs_.NOB_1.ID_135" not in mutated_project_dir:
            continue
        SpectrumCoverageManager.rebuild_spectrum_coverage_with_target_coverage(mutated_project_dir=mutated_project_dir,
                                                                               target_coverage=target_coverage)

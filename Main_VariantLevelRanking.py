import logging
import os

from FileManager import get_failing_variants, get_variants_dir, list_dir, get_all_variant_dirs, \
    get_spectrum_failed_coverage_file_name_with_version, join_path, get_test_coverage_dir, \
    get_spectrum_passed_coverage_file_name_with_version
from ranking.RankingManager import  get_all_stms_of_the_system, get_all_suspicious_stm
from ranking.Spectrum_Expression import TARANTULA
from ranking.VariantLevelRankingManager import get_num_passing_failing_variants, calculate_suspiciousness_variant_level

if __name__ == "__main__":
    mutated_project_dir = "/home/huent/Documents/Trang/temp/Single_Bug/BankAccountTP/4wise/mutated_projects/_MultipleBugs_.NOB_1.ID_160"
    failing_variants = get_failing_variants(mutated_project_dir)

    all_stms_of_the_system = get_all_stms_of_the_system(mutated_project_dir, "", 0.0)
    failing_passing_variants_of_stms, total_fails, total_passes = get_num_passing_failing_variants(mutated_project_dir, all_stms_of_the_system, spectrum_coverage_prefix="")

    variant_level_suspicousness = calculate_suspiciousness_variant_level(failing_passing_variants_of_stms, total_fails, total_passes, TARANTULA)
    print(variant_level_suspicousness)
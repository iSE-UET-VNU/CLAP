import os

from ranking.RankingResultManager import ranking_with_coverage_rate
from FileManager import join_path
from ranking.Spectrum_Expression import JACCARD, SORENSEN_DICE, TARANTULA, OCHIAI, OP2, BARINEL, DSTAR, ROGERS_TANIMOTO, AMPLE, \
    SIMPLE_MATCHING, RUSSELL_RAO, COHEN, SCOTT, ROGOT1, GEOMETRIC_MEAN, M2, WONG1, SOKAL, DICE, HUMANN, OVERLAP, ZOLTAR, \
    WONG3, WONG2, M1, ROGOT2, EUCLID, HAMMING, FLEISS, ANDERBERG, KULCZYNSKI1, KULCZYNSKI2, HARMONIC_MEAN, GOODMAN

if __name__ == "__main__":
    #result_folder = "coverage_" + spectrum_coverage_prefix + "_"
    result_folder = ""
    base_dir = "/home/huent/Documents/Trang/single_bugs/"
    system_names = ["ZipMe"]
    project_names = ["4wise"]
    #multiple_coverages = ["INoT_1_", "INoT_2_", "INoT_3_", "INoT_4_", "INoT_5_", "INoT_6_", "INoT_7_", "INoT_8_", "INoT_9_", "INoT_10_"]
    multiple_coverages = [""]
    for spectrum_coverage_prefix in multiple_coverages:
        #result_folder = "coverage_" + spectrum_coverage_prefix + "_"

        filtering_coverage_rate_list = [0.0]
        for coverage_index in range(0, len(filtering_coverage_rate_list)):
            for system in system_names:
                 system_dir = join_path(base_dir, system)
                 print(system)
                 for project_index in range(0, len(project_names)):
                     k_wise_dir = join_path(system_dir, project_names[project_index])
                     print(k_wise_dir)
                     if os.path.isdir(k_wise_dir):
                        #ranking_with_coverage_rate(base_dir, project_names[project_index], filtering_coverage_rate_list[coverage_index], [TARANTULA, OCHIAI, OP2, BARINEL, DSTAR])
                        ranking_with_coverage_rate(result_folder, system_dir, system, project_names[project_index],
                                                   filtering_coverage_rate_list[coverage_index],
                                                   [TARANTULA, OCHIAI, OP2, BARINEL, DSTAR,
                                                    RUSSELL_RAO, SIMPLE_MATCHING, ROGERS_TANIMOTO, AMPLE, JACCARD,
                                                    COHEN, SCOTT, ROGOT1, GEOMETRIC_MEAN, M2,
                                                    WONG1, SOKAL, SORENSEN_DICE, DICE, HUMANN,
                                                    M1, WONG2, WONG3, ZOLTAR, OVERLAP,
                                                    EUCLID, ROGOT2, HAMMING, FLEISS, ANDERBERG,
                                                    GOODMAN, HARMONIC_MEAN, KULCZYNSKI1, KULCZYNSKI2],
                                                   spectrum_coverage_prefix)
                        # ranking_with_coverage_rate(result_folder, system_dir, system, project_names[project_index],
                        #                           filtering_coverage_rate_list[coverage_index],
                        #                           [JACCARD, SORENSEN_DICE], spectrum_coverage_prefix)





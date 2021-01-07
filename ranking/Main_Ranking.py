import os

from ranking.RankingResultManager import ranking_with_coverage_rate
from FileManager import join_path
from Spectrum_Expression import JACCARD, SORENSEN_DICE

if __name__ == "__main__":
    #result_folder = "coverage_" + spectrum_coverage_prefix + "_"
    result_folder = "Example_"
    base_dir = "/Users/thu-trangnguyen/OneDrive/Research/SPL systems/data/"
    system_names = ["BankAccountTP"]
    project_names = ["4wise"]

    spectrum_coverage_prefix = ""

    filtering_coverage_rate_list = [0.95]
    for coverage_index in range(0, len(filtering_coverage_rate_list)):
        for system in system_names:
             system_dir = join_path(base_dir, system)
             print(system)
             for project_index in range(0, len(project_names)):
                 k_wise_dir = join_path(system_dir, project_names[project_index])
                 print(k_wise_dir)
                 if os.path.isdir(k_wise_dir):
                    #ranking_with_coverage_rate(base_dir, project_names[project_index], filtering_coverage_rate_list[coverage_index], [TARANTULA, OCHIAI, OP2, BARINEL, DSTAR])
                    # ranking_with_coverage_rate(system_dir, system, project_names[project_index],
                    #                            filtering_coverage_rate_list[coverage_index],
                    #                            [TARANTULA, OCHIAI, OP2, BARINEL, DSTAR,
                    #                             RUSSELL_RAO, SIMPLE_MATCHING, ROGERS_TANIMOTO, AMPLE, JACCARD,
                    #                             COHEN, SCOTT, ROGOT1, GEOMETRIC_MEAN, M2,
                    #                             WONG1, SOKAL, SORENSEN_DICE, DICE, HUMANN,
                    #                             M1, WONG2, WONG3, ZOLTAR, OVERLAP,
                    #                             EUCLID, ROGOT2, HAMMING, FLEISS, ANDERBERG,
                    #                             GOODMAN, HARMONIC_MEAN, KULCZYNSKI1, KULCZYNSKI2],
                    #                            spectrum_coverage_prefix)
                    ranking_with_coverage_rate(result_folder, system_dir, system, project_names[project_index],
                                              filtering_coverage_rate_list[coverage_index],
                                              [JACCARD, SORENSEN_DICE], spectrum_coverage_prefix)





import os
import threading

from ExperimentResultManager import ranking_with_coverage_rate
from FileManager import join_path
from Spectrum_Expression import RUSSELL_RAO, SIMPLE_MATCHING, ROGERS_TANIMOTO, AMPLE, JACCARD, COHEN, SCOTT, ROGOT1, \
    GEOMETRIC_MEAN, M2, TARANTULA, OCHIAI, OP2, BARINEL, DSTAR, WONG1, SOKAL, KULCZYNSKI2, GOODMAN, HARMONIC_MEAN, \
    EUCLID, KULCZYNSKI1, WONG2, M1, WONG3, ROGOT2, HAMMING, FLEISS, ANDERBERG, ZOLTAR, OVERLAP, SORENSEN_DICE, DICE, \
    HUMANN

if __name__ == "__main__":

    base_dir = "/Users/thu-trangnguyen/Documents/Research/configurable_system/Experiment/projects/"
    system_names = ["ExamDB_Test"]
    project_names = ["1wise", "2wise", "3wise", "4wise", "5wise"]

    spectrum_coverage_prefix = "v3__"

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
                    ranking_with_coverage_rate(system_dir, system, project_names[project_index],
                                               filtering_coverage_rate_list[coverage_index],
                                               [TARANTULA, OCHIAI, OP2, BARINEL, DSTAR,
                                                RUSSELL_RAO, SIMPLE_MATCHING, ROGERS_TANIMOTO, AMPLE, JACCARD,
                                                COHEN, SCOTT, ROGOT1, GEOMETRIC_MEAN, M2,
                                                WONG1, SOKAL, SORENSEN_DICE, DICE, HUMANN,
                                                M1, WONG2, WONG3, ZOLTAR, OVERLAP,
                                                EUCLID, ROGOT2, HAMMING, FLEISS, ANDERBERG,
                                                GOODMAN, HARMONIC_MEAN, KULCZYNSKI1, KULCZYNSKI2],
                                               spectrum_coverage_prefix)
                    #ranking_with_coverage_rate(system_dir, system, project_names[project_index],
                    #                           filtering_coverage_rate_list[coverage_index],
                    #                           [TARANTULA], spectrum_coverage_prefix)





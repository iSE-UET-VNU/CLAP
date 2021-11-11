from FileManager import join_path
from ranking.MultipleBugsManager import multiple_bugs_ranking
from ranking.Spectrum_Expression import JACCARD, SORENSEN_DICE, TARANTULA, OCHIAI, OP2, BARINEL, DSTAR, ROGERS_TANIMOTO, \
    AMPLE, \
    SIMPLE_MATCHING, RUSSELL_RAO, COHEN, SCOTT, ROGOT1, GEOMETRIC_MEAN, M2, WONG1, SOKAL, DICE, HUMANN, OVERLAP, ZOLTAR, \
    WONG3, WONG2, M1, ROGOT2, EUCLID, HAMMING, FLEISS, ANDERBERG, KULCZYNSKI1, KULCZYNSKI2, HARMONIC_MEAN, GOODMAN

if __name__ == "__main__":
    result_base_folder = "temp_"
    data_base_dir = "/Users/thu-trangnguyen/Downloads/VarCop/Debug"
    system_names = ["BankAccountTP"]
    bug_folders = ["2Bug"]
    alpha = [0.5]
    # alpha = [1, 0.3, 0.7]
    kwise_list = ["4wise"]
    filtering_coverage_rate_list = [0.0]
    # coverage_versions = [ "INoT_2_", "INoT_4_", "INoT_6_", "INoT_8_", "INoT_9_"]
    coverage_versions = [""]
    for k in alpha:
        result_folder = result_base_folder + str(k)
        for system_name in system_names:
            system_dir = join_path(data_base_dir, system_name)
            for bug_folder in bug_folders:
                bug_folder_dir = join_path(system_dir, bug_folder)
                for kwise in kwise_list:
                    for coverage in coverage_versions:
                        multiple_bugs_ranking(result_folder, system_name, bug_folder, bug_folder_dir, kwise,
                                              [TARANTULA, OCHIAI, OP2, BARINEL, DSTAR,
                                               RUSSELL_RAO, SIMPLE_MATCHING, ROGERS_TANIMOTO, AMPLE, JACCARD,
                                               COHEN, SCOTT, ROGOT1, GEOMETRIC_MEAN, M2,
                                               WONG1, SOKAL, SORENSEN_DICE, DICE, HUMANN,
                                               WONG2, EUCLID, ZOLTAR,
                                               ROGOT2, HAMMING, FLEISS, ANDERBERG,
                                               GOODMAN, HARMONIC_MEAN, KULCZYNSKI2], 0.0, coverage, k)

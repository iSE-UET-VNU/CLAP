from FileManager import join_path
from consistent_testing_manager.FileName import classified_all_file, classified_all_single_bug_file
from ranking.MultipleBugsManager import multiple_bugs_ranking
from spectrum_manager.Spectrum_Expression import JACCARD, SORENSEN_DICE, TARANTULA, OCHIAI, OP2, BARINEL, DSTAR, ROGERS_TANIMOTO, \
    AMPLE, \
    SIMPLE_MATCHING, RUSSELL_RAO, COHEN, SCOTT, ROGOT1, GEOMETRIC_MEAN, M2, WONG1, SOKAL, DICE, HUMANN, ZOLTAR, \
    WONG2, ROGOT2, EUCLID, HAMMING, FLEISS, ANDERBERG, KULCZYNSKI2, HARMONIC_MEAN, GOODMAN

SBFL_METRICS = [TARANTULA, OCHIAI, OP2, BARINEL, DSTAR,
                RUSSELL_RAO, SIMPLE_MATCHING, ROGERS_TANIMOTO, AMPLE, JACCARD,
                COHEN, SCOTT, ROGOT1, GEOMETRIC_MEAN, M2,
                WONG1, SOKAL, SORENSEN_DICE, DICE, HUMANN,
                WONG2, EUCLID, ZOLTAR,
                ROGOT2, HAMMING, FLEISS, ANDERBERG,
                GOODMAN, HARMONIC_MEAN, KULCZYNSKI2]

if __name__ == "__main__":
    result_base_folder = "classified_all_keep_tests_ddu1_"
    data_base_dir = "/Users/thu-trangnguyen/Documents/Research/SPL"
    system_names = ["GPL"]
    bug_folders = [ "1Bug"]
    alpha = [0.5]
    # alpha = [1, 0.3, 0.7]
    kwise_list = ["1wise", "2wise", "4wise"]
    keep_useful_tests = True

    for k in alpha:
        result_folder = result_base_folder + str(k)
        for system_name in system_names:
            system_dir = join_path(data_base_dir, system_name)
            for bug_folder in bug_folders:
                bug_folder_dir = join_path(system_dir, bug_folder)
                for kwise in kwise_list:
                    multiple_bugs_ranking(result_folder, system_name, bug_folder, bug_folder_dir, kwise, SBFL_METRICS, k, classified_all_file, keep_useful_tests)
                    #multiple_bugs_ranking(result_folder, system_name, bug_folder, bug_folder_dir, kwise, [TARANTULA], k, classified_all_file, keep_useful_tests)

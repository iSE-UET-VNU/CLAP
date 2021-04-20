from FileManager import join_path
from ranking.MultipleBugsManager import mutiple_bugs_ranking
from ranking.SBFLOnly_MultipleBugsManager import sbfl_only_mutiple_bugs_ranking
from ranking.Spectrum_Expression import JACCARD, SORENSEN_DICE, TARANTULA, OCHIAI, OP2, BARINEL, DSTAR, ROGERS_TANIMOTO, AMPLE, \
    SIMPLE_MATCHING, RUSSELL_RAO, COHEN, SCOTT, ROGOT1, GEOMETRIC_MEAN, M2, WONG1, SOKAL, DICE, HUMANN, OVERLAP, ZOLTAR, \
    WONG3, WONG2, M1, ROGOT2, EUCLID, HAMMING, FLEISS, ANDERBERG, KULCZYNSKI1, KULCZYNSKI2, HARMONIC_MEAN, GOODMAN


if __name__ == "__main__":
    result_folder = "DataV2_Results"
    base_dir = "/home/huent/Documents/Trang/temp/"
    system_names = ["BankAccountTP"]
    bug_folders = ["2Bug"]
    filtering_coverage_rate_list = [0.0]
    for system_name in system_names:
        system_dir = join_path(base_dir, system_name)
        for bug_folder in bug_folders:
            bug_folder_dir = join_path(system_dir, bug_folder)
            for coverage in filtering_coverage_rate_list:
                print(bug_folder_dir)
                # mutiple_bugs_ranking(result_folder, system_name, system_dir, [TARANTULA, OCHIAI, OP2, BARINEL, DSTAR,
                #                 #                                         RUSSELL_RAO, SIMPLE_MATCHING, ROGERS_TANIMOTO, AMPLE, JACCARD,
                #                 #                                         COHEN, SCOTT, ROGOT1, GEOMETRIC_MEAN, M2,
                #                 #                                         WONG1, SOKAL, SORENSEN_DICE, DICE, HUMANN,
                #                 #                                          WONG2, EUCLID, ZOLTAR,
                #                 #                                          ROGOT2, HAMMING, FLEISS, ANDERBERG,
                #                 #                                         GOODMAN, HARMONIC_MEAN, KULCZYNSKI2], coverage)
                mutiple_bugs_ranking(result_folder, system_name, bug_folder,  bug_folder_dir, [TARANTULA, OCHIAI], coverage)
                # sbfl_only_mutiple_bugs_ranking(result_folder, system_name, bug_folder, bug_folder_dir, [TARANTULA, OCHIAI, OP2, BARINEL, DSTAR,
                #                                         RUSSELL_RAO, SIMPLE_MATCHING, ROGERS_TANIMOTO, AMPLE, JACCARD,
                #                                         COHEN, SCOTT, ROGOT1, GEOMETRIC_MEAN, M2,
                #                                         WONG1, SOKAL, SORENSEN_DICE, DICE, HUMANN,
                #                                          WONG2, EUCLID, ZOLTAR,
                #                                          ROGOT2, HAMMING, FLEISS, ANDERBERG,
                #                                         GOODMAN, HARMONIC_MEAN, KULCZYNSKI2], coverage)
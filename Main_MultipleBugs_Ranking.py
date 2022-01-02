from FileManager import join_path
from consistent_testing_manager.FileName import *
from ranking.MultipleBugsManager import multiple_bugs_ranking
from spectrum_manager.Spectrum_Expression import JACCARD, SORENSEN_DICE, TARANTULA, OCHIAI, OP2, BARINEL, DSTAR, \
    ROGERS_TANIMOTO, \
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
    # system_dir is the path of folder which contains mutated projects
    system_dir = "/Users/thu-trangnguyen/Documents/Research/SPL/Debug/3Bug/4wise"

    # the corresponding system name, num of bug and kwise
    system_name = "Debug"
    num_of_bugs = "3Bug"
    kwise = "4wise"

    # FP_detection can be True or False
    FP_detections = [False, True]
    # add_more_tests can be True or False
    # if FP_detection is False, don't need to care about the value of add_more_testsMul
    Add_tests = [False, True]

    for FP_detection in FP_detections:
        add_more_tests = False
        if FP_detection:
            for test in Add_tests:
                add_more_tests = test
                if not FP_detection:
                    result_folder = "original"
                elif not add_more_tests:
                    result_folder = "remove_FPs"
                else:
                    result_folder = "add_more_tests"
                multiple_bugs_ranking(result_folder=result_folder, system_name=system_name, num_of_bugs=num_of_bugs,
                                      system_dir=system_dir, kwise=kwise, spectrum_expressions=SBFL_METRICS,
                                      FP_detection=FP_detection, classified_file_name=classified_all_cases_file,
                                      add_more_tests=add_more_tests)
                # multiple_bugs_ranking(result_folder=result_folder, system_name=system_name, num_of_bugs=num_of_bugs,
                #                       system_dir=system_dir, kwise=kwise, spectrum_expressions=[OCHIAI],
                #                       FP_detection=FP_detection, classified_file_name=classified_all_cases_file,
                #                       add_more_tests=add_more_tests)
        else:
            if not FP_detection:
                result_folder = "original"
            elif not add_more_tests:
                result_folder = "remove_FPs"
            else:
                result_folder = "add_more_tests"
            multiple_bugs_ranking(result_folder=result_folder, system_name=system_name, num_of_bugs=num_of_bugs,
                                  system_dir=system_dir, kwise=kwise, spectrum_expressions=SBFL_METRICS,
                                  FP_detection=FP_detection, classified_file_name=classified_all_cases_file,
                                  add_more_tests=add_more_tests)
            # multiple_bugs_ranking(result_folder=result_folder, system_name=system_name, num_of_bugs=num_of_bugs,
            #                       system_dir=system_dir, kwise=kwise, spectrum_expressions=[OCHIAI],
            #                       FP_detection=FP_detection, classified_file_name=classified_all_cases_file,
            #                       add_more_tests=add_more_tests)

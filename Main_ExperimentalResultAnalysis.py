import pandas as pandas

from ExperimentalResultsAnalyzer import summary_result, summary_for_same_bugs, count_total_bugs, summary_hitx, \
    write_all_bugs_to_a_file
from FileManager import join_path, EXPERIMENT_RESULT_FOLDER
from Spectrum_Expression import WONG3

if __name__ == "__main__":
    all_bugs_file_dir = join_path(EXPERIMENT_RESULT_FOLDER,
                                  "all_bugs_normalization_2.xlsx")
    # file_lists = [
    #     "/Users/trangnt/Documents/Projects/experiment_results/AGGREGATION_AVERAGE_ADDITION_NORMALIZATION1/BankAccountTP/4wise/0.95_.xlsx",
    #     "/Users/trangnt/Documents/Projects/experiment_results/AGGREGATION_AVERAGE_ADDITION_NORMALIZATION1/Elevator/4wise/0.95_.xlsx",
    #     "/Users/trangnt/Documents/Projects/experiment_results/AGGREGATION_AVERAGE_ADDITION_NORMALIZATION1/Email/4wise/0.95_.xlsx",
    #     "/Users/trangnt/Documents/Projects/experiment_results/AGGREGATION_AVERAGE_ADDITION_NORMALIZATION1/ExamDB/4wise/0.95_.xlsx",
    #     "/Users/trangnt/Documents/Projects/experiment_results/AGGREGATION_AVERAGE_ADDITION_NORMALIZATION1/GPL/4wise/0.95_.xlsx"
    # ]
    # write_all_bugs_to_a_file(all_bugs_file_dir, file_lists)
    #
    # summary_file = join_path(EXPERIMENT_RESULT_FOLDER,
    #                              "summary_normalization_2.xlsx")
    # summary_result(all_bugs_file_dir, summary_file)


    #num_of_program_stms = {"BankAccountTP": 143, "Elevator": 854, "Email": 439, "ExamDB": 513, "GPL": 1944}
    # summary_file_dir = join_path(EXPERIMENT_RESULT_FOLDER,
    #                              "summary_same_bug.xlsx")
    # files_list = {
    #     "1wise": "/Users/trangnt/Documents/Projects/experiment_results/AGGREGATION_AVERAGE_ADDITION_NORMALIZATION1/BankAccountTP/1wise/0.95_.xlsx",
    #     "2wise": "/Users/trangnt/Documents/Projects/experiment_results/AGGREGATION_AVERAGE_ADDITION_NORMALIZATION1/BankAccountTP/2wise/0.95_.xlsx",
    #     "3wise": "/Users/trangnt/Documents/Projects/experiment_results/AGGREGATION_AVERAGE_ADDITION_NORMALIZATION1/BankAccountTP/3wise/0.95_.xlsx",
    #     "4wise": "/Users/trangnt/Documents/Projects/experiment_results/AGGREGATION_AVERAGE_ADDITION_NORMALIZATION1/BankAccountTP/4wise/0.95_.xlsx"
    #     }
    # summary_for_same_bugs(summary_file_dir, files_list, 143)

    hitx_file_dir = join_path(EXPERIMENT_RESULT_FOLDER,
                                 "hitx_.xlsx")
    summary_hitx(hitx_file_dir, all_bugs_file_dir)

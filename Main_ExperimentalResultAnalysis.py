import pandas as pandas

from ExperimentalResultsAnalyzer import summary_result, summary_for_same_bugs, count_total_bugs, summary_hitx, \
    write_all_bugs_to_a_file
from FileManager import join_path, EXPERIMENT_RESULT_FOLDER
from Spectrum_Expression import WONG3

if __name__ == "__main__":
    all_bugs_file_dir = join_path(EXPERIMENT_RESULT_FOLDER,
                                  "all_bugs_arithmetic_mean_normalization_alpha_beta.xlsx")
    file_lists = [
        "/Users/thu-trangnguyen/Documents/project/InputPreparation/experiment_results/AGGREGATION_ARITHMETIC_MEAN_NORMALIZATION_ALPHA_BETA/BankAccountTP/4wise/0.95_.xlsx",
        "/Users/thu-trangnguyen/Documents/project/InputPreparation/experiment_results/AGGREGATION_ARITHMETIC_MEAN_NORMALIZATION_ALPHA_BETA/Elevator/4wise/0.95_.xlsx",
        "/Users/thu-trangnguyen/Documents/project/InputPreparation/experiment_results/AGGREGATION_ARITHMETIC_MEAN_NORMALIZATION_ALPHA_BETA/Email/4wise/0.95_.xlsx",
        "/Users/thu-trangnguyen/Documents/project/InputPreparation/experiment_results/AGGREGATION_ARITHMETIC_MEAN_NORMALIZATION_ALPHA_BETA/ExamDB/4wise/0.95_.xlsx",
        "/Users/thu-trangnguyen/Documents/project/InputPreparation/experiment_results/AGGREGATION_ARITHMETIC_MEAN_NORMALIZATION_ALPHA_BETA/GPL/4wise/0.95_.xlsx"
    ]
    write_all_bugs_to_a_file(all_bugs_file_dir, file_lists)

    summary_file = join_path(EXPERIMENT_RESULT_FOLDER,
                                "summary_arithmetic_mean_normalization_alpha_beta.xlsx")
    summary_result(all_bugs_file_dir, summary_file)


    # num_of_program_stms = {"BankAccountTP": 143, "Elevator": 854, "Email": 439, "ExamDB": 513, "GPL": 1944}
    # summary_file_dir = join_path(EXPERIMENT_RESULT_FOLDER,
    #                              "summary_same_bug_gpl.xlsx")
    # files_list = {
    #     "1wise": "/Users/thu-trangnguyen/Documents/project/InputPreparation/experiment_results/AGGREGATION_ARITHMETIC_MEAN_NORMALIZATION_ALPHA_BETA/GPL/1wise/0.8_.xlsx",
    #     "2wise": "/Users/thu-trangnguyen/Documents/project/InputPreparation/experiment_results/AGGREGATION_ARITHMETIC_MEAN_NORMALIZATION_ALPHA_BETA/GPL/2wise/0.8_.xlsx",
    #     "3wise": "/Users/thu-trangnguyen/Documents/project/InputPreparation/experiment_results/AGGREGATION_ARITHMETIC_MEAN_NORMALIZATION_ALPHA_BETA/GPL/3wise/0.8_.xlsx",
    #     "4wise": "/Users/thu-trangnguyen/Documents/project/InputPreparation/experiment_results/AGGREGATION_ARITHMETIC_MEAN_NORMALIZATION_ALPHA_BETA/GPL/4wise/0.8_.xlsx"
    #     }
    # summary_for_same_bugs(summary_file_dir, files_list, 1944)

    # hitx_file_dir = join_path(EXPERIMENT_RESULT_FOLDER,
    #                              "hitx_arithmetic_mean_normalization_none.xlsx")
    # summary_hitx(hitx_file_dir, all_bugs_file_dir)

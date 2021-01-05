from experimental_results_analyzer.ExperimentalResultsAnalyzer import summary_result, summary_hitx, \
    write_all_bugs_to_a_file
from FileManager import join_path, EXPERIMENT_RESULT_FOLDER
from MB_ExperimentalResultsAnalyzer import percentage_of_bugs_found, average_best_rank, average_worst_rank, \
    num_of_case_found_bugs
from ranking.Spectrum_Expression import OCHIAI


def summary_single_bugs():
    all_bugs_file_dir = join_path(EXPERIMENT_RESULT_FOLDER,
                                  "2021_0105.xlsx")
    file_lists = [
        "/Users/thu-trangnguyen/Documents/project/InputPreparation/experiment_results/AGGREGATION_ARITHMETIC_MEAN_NORMALIZATION_ALPHA_BETA/BankAccountTP/4wise/0.95_.xlsx",
        "/Users/thu-trangnguyen/Documents/project/InputPreparation/experiment_results/AGGREGATION_ARITHMETIC_MEAN_NORMALIZATION_ALPHA_BETA/Elevator/4wise/0.95_.xlsx"
    ]
    write_all_bugs_to_a_file(all_bugs_file_dir, file_lists)

    summary_file = join_path(EXPERIMENT_RESULT_FOLDER,
                             "2021_0105_summary.xlsx")
    summary_result(all_bugs_file_dir, summary_file)
    hitx_file_dir = join_path(EXPERIMENT_RESULT_FOLDER,
                              "hitx_2021_0105.xlsx")
    summary_hitx(hitx_file_dir, all_bugs_file_dir)

def summary_multiple_bugs():
    all_bugs_file_dir = join_path(EXPERIMENT_RESULT_FOLDER,
                                  "2021_0105_multiple_bugs.xlsx")
    file_lists = [
          "/Users/thu-trangnguyen/Documents/project/InputPreparation/experiment_results/Multiple_bugs_AGGREGATION_ARITHMETIC_MEAN_NORMALIZATION_ALPHA_BETA/BankAccountTP2new/0.0_.xlsx",
        "/Users/thu-trangnguyen/Documents/project/InputPreparation/experiment_results/Multiple_bugs_AGGREGATION_ARITHMETIC_MEAN_NORMALIZATION_ALPHA_BETA/BankAccountTP3new/0.0_.xlsx",
        "/Users/thu-trangnguyen/Documents/project/InputPreparation/experiment_results/Multiple_bugs_AGGREGATION_ARITHMETIC_MEAN_NORMALIZATION_ALPHA_BETA/Elevator2new/0.1_.xlsx",
        "/Users/thu-trangnguyen/Documents/project/InputPreparation/experiment_results/Multiple_bugs_AGGREGATION_ARITHMETIC_MEAN_NORMALIZATION_ALPHA_BETA/Elevator3new/0.1_.xlsx",
        "/Users/thu-trangnguyen/Documents/project/InputPreparation/experiment_results/Multiple_bugs_AGGREGATION_ARITHMETIC_MEAN_NORMALIZATION_ALPHA_BETA/Email2new/0.0_.xlsx",
        "/Users/thu-trangnguyen/Documents/project/InputPreparation/experiment_results/Multiple_bugs_AGGREGATION_ARITHMETIC_MEAN_NORMALIZATION_ALPHA_BETA/Email3new/0.0_.xlsx",
        "/Users/thu-trangnguyen/Documents/project/InputPreparation/experiment_results/Multiple_bugs_AGGREGATION_ARITHMETIC_MEAN_NORMALIZATION_ALPHA_BETA/ExamDB2new/0.0_.xlsx",
        "/Users/thu-trangnguyen/Documents/project/InputPreparation/experiment_results/Multiple_bugs_AGGREGATION_ARITHMETIC_MEAN_NORMALIZATION_ALPHA_BETA/ExamDB3new/0.0_.xlsx",
        "/Users/thu-trangnguyen/Documents/project/InputPreparation/experiment_results/Multiple_bugs_AGGREGATION_ARITHMETIC_MEAN_NORMALIZATION_ALPHA_BETA/GPL/0.0_.xlsx",
        "/Users/thu-trangnguyen/Documents/project/InputPreparation/experiment_results/Multiple_bugs_AGGREGATION_ARITHMETIC_MEAN_NORMALIZATION_ALPHA_BETA/GPL3/0.0_.xlsx"
    ]
    #write_all_bugs_to_a_file(all_bugs_file_dir, file_lists)
    examined_statements = [1, 2, 3]
    result_percentage_found_bugs = percentage_of_bugs_found(all_bugs_file_dir, OCHIAI, examined_statements)
    print(result_percentage_found_bugs)
    average_best_rank(all_bugs_file_dir, OCHIAI)
    average_worst_rank(all_bugs_file_dir, OCHIAI)
    result_case_found_bugs = num_of_case_found_bugs(all_bugs_file_dir, OCHIAI, examined_statements)
    print(result_case_found_bugs)

if __name__ == "__main__":
    #summary_single_bugs()
    summary_multiple_bugs()
    # all_bugs_file_dir = join_path(EXPERIMENT_RESULT_FOLDER,
    #                               "multiple_bugs_2021_01_03.xlsx")
    # file_lists = [
    #       "/Users/thu-trangnguyen/Documents/project/InputPreparation/experiment_results/Multiple_bugs_AGGREGATION_ARITHMETIC_MEAN_NORMALIZATION_ALPHA_BETA/BankAccountTP2new/0.0_.xlsx",
    #     "/Users/thu-trangnguyen/Documents/project/InputPreparation/experiment_results/Multiple_bugs_AGGREGATION_ARITHMETIC_MEAN_NORMALIZATION_ALPHA_BETA/BankAccountTP3new/0.0_.xlsx",
    #     "/Users/thu-trangnguyen/Documents/project/InputPreparation/experiment_results/Multiple_bugs_AGGREGATION_ARITHMETIC_MEAN_NORMALIZATION_ALPHA_BETA/Elevator2new/0.1_.xlsx",
    #     "/Users/thu-trangnguyen/Documents/project/InputPreparation/experiment_results/Multiple_bugs_AGGREGATION_ARITHMETIC_MEAN_NORMALIZATION_ALPHA_BETA/Elevator3new/0.1_.xlsx",
    #     "/Users/thu-trangnguyen/Documents/project/InputPreparation/experiment_results/Multiple_bugs_AGGREGATION_ARITHMETIC_MEAN_NORMALIZATION_ALPHA_BETA/Email2new/0.0_.xlsx",
    #     "/Users/thu-trangnguyen/Documents/project/InputPreparation/experiment_results/Multiple_bugs_AGGREGATION_ARITHMETIC_MEAN_NORMALIZATION_ALPHA_BETA/Email3new/0.0_.xlsx",
    #     "/Users/thu-trangnguyen/Documents/project/InputPreparation/experiment_results/Multiple_bugs_AGGREGATION_ARITHMETIC_MEAN_NORMALIZATION_ALPHA_BETA/ExamDB2new/0.0_.xlsx",
    #     "/Users/thu-trangnguyen/Documents/project/InputPreparation/experiment_results/Multiple_bugs_AGGREGATION_ARITHMETIC_MEAN_NORMALIZATION_ALPHA_BETA/ExamDB3new/0.0_.xlsx",
    #     "/Users/thu-trangnguyen/Documents/project/InputPreparation/experiment_results/Multiple_bugs_AGGREGATION_ARITHMETIC_MEAN_NORMALIZATION_ALPHA_BETA/GPL/0.0_.xlsx",
    #     "/Users/thu-trangnguyen/Documents/project/InputPreparation/experiment_results/Multiple_bugs_AGGREGATION_ARITHMETIC_MEAN_NORMALIZATION_ALPHA_BETA/GPL3/0.0_.xlsx"
    # ]
    # write_all_bugs_to_a_file(all_bugs_file_dir, file_lists)
    #
    # summary_file = join_path(EXPERIMENT_RESULT_FOLDER,
    #                             "summary_arithmetic_mean_normalization_alpha_beta.xlsx")
    # summary_result(all_bugs_file_dir, summary_file)


    # num_of_program_stms = {"BankAccountTP": 143, "Elevator": 854, "Email": 439, "ExamDB": 513, "GPL": 1944}
    # summary_file_dir = join_path(EXPERIMENT_RESULT_FOLDER,
    #                              "coverage_INoT_10.xlsx")
    # files_list = {
    #     "4wise": "/Users/thu-trangnguyen/Documents/project/InputPreparation/experiment_results/coverage_INoT_10___AGGREGATION_ARITHMETIC_MEAN_NORMALIZATION_ALPHA_BETA/ExamDB/4wise/0.95_.xlsx"
    # }
    # summary_for_same_bugs(summary_file_dir, files_list, 513)

    # hitx_file_dir = join_path(EXPERIMENT_RESULT_FOLDER,
    #                              "hitx_arithmetic_mean_normalization_none.xlsx")
    # summary_hitx(hitx_file_dir, all_bugs_file_dir)


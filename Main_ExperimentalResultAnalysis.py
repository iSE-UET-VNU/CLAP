from experimental_results_analyzer.ExperimentalResultsAnalyzer import summary_result, summary_hitx, \
    write_all_bugs_to_a_file
from FileManager import join_path, EXPERIMENT_RESULT_FOLDER
from experimental_results_analyzer.MB_ExperimentalResultsAnalyzer import percentage_of_bugs_found, \
    num_of_case_found_bugs, average_worst_rank, average_best_rank

from ranking.Spectrum_Expression import OCHIAI, TARANTULA, OP2


def summary_single_bugs():
    all_bugs_file_dir = join_path(EXPERIMENT_RESULT_FOLDER,
                                  "all_bugs.xlsx")
    file_lists = [
        "/Users/thu-trangnguyen/Documents/project/InputPreparation/experiment_results/public/AGGREGATION_ARITHMETIC_MEAN_NORMALIZATION_ALPHA_BETA/BankAccountTP/4wise/ranking_results.xlsx",
        "/Users/thu-trangnguyen/Documents/project/InputPreparation/experiment_results/public/AGGREGATION_ARITHMETIC_MEAN_NORMALIZATION_ALPHA_BETA/Elevator/4wise/ranking_results.xlsx"
    ]
    write_all_bugs_to_a_file(all_bugs_file_dir, file_lists)

    summary_file = join_path(EXPERIMENT_RESULT_FOLDER,
                             "all_bugs_summary.xlsx")
    summary_result(all_bugs_file_dir, summary_file)
    hitx_file_dir = join_path(EXPERIMENT_RESULT_FOLDER,
                              "all_bugs_hix.xlsx")
    summary_hitx(hitx_file_dir, all_bugs_file_dir)



def summary_multiple_bugs():
    all_bugs_file_dir = join_path(EXPERIMENT_RESULT_FOLDER,
                                  "2021_0118_multiple_bugs.xlsx")
    file_lists = [
      "/Users/thu-trangnguyen/Documents/project/InputPreparation/experiment_results/public/multiple_bugs_AGGREGATION_ARITHMETIC_MEAN_NORMALIZATION_ALPHA_BETA/BankAccountTP/ranking_results.xlsx",
      "/Users/thu-trangnguyen/Documents/project/InputPreparation/experiment_results/public/multiple_bugs_AGGREGATION_ARITHMETIC_MEAN_NORMALIZATION_ALPHA_BETA/BankAccountTP2new/ranking_results.xlsx",
      "/Users/thu-trangnguyen/Documents/project/InputPreparation/experiment_results/public/multiple_bugs_AGGREGATION_ARITHMETIC_MEAN_NORMALIZATION_ALPHA_BETA/Elevator/ranking_results.xlsx"

    ]
    write_all_bugs_to_a_file(all_bugs_file_dir, file_lists)
    examined_statements = [1, 2, 3, 4, 5,]
    result_percentage_found_bugs = percentage_of_bugs_found(all_bugs_file_dir, OCHIAI, examined_statements)
    print(result_percentage_found_bugs)
    print("best", average_best_rank(all_bugs_file_dir, OCHIAI))
    print("worst", average_worst_rank(all_bugs_file_dir, OCHIAI))
    result_case_found_bugs = num_of_case_found_bugs(all_bugs_file_dir, OCHIAI, examined_statements)
    print(result_case_found_bugs)


if __name__ == "__main__":

    #summary_single_bugs()
    summary_multiple_bugs()





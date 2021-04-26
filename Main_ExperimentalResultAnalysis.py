from experimental_results_analyzer.ExperimentalResultsAnalyzer import summary_result, summary_hitx, \
    write_all_bugs_to_a_file
from FileManager import join_path, EXPERIMENT_RESULT_FOLDER
from experimental_results_analyzer.ForAssumptionEvalutation_ExperimentalResultAnalyzer import assumption_summary_result, \
    assumption_summary_hitx
from experimental_results_analyzer.MB_ExperimentalResultsAnalyzer import percentage_of_bugs_found, \
    num_of_case_found_bugs, average_worst_rank, average_best_rank
from experimental_results_analyzer.SBFL_ONLY_ExperimentalResultsAnalyzer import sbfl_only_write_all_bugs_to_a_file, \
    sbfl_only_summary_result, sbfl_only_summary_hitx, SPECTRUM_EXPRESSIONS_LIST
from experimental_results_analyzer.SBFL_ONLY_MB_ExperimentalResultsAnalyzer import sbfl_only_percentage_of_bugs_found, \
    sbfl_only_average_best_rank, sbfl_only_average_worst_rank, sbfl_only_num_of_case_found_bugs, \
    sbfl_only_average_best_exam, sbfl_only_average_worst_exam

from ranking.Spectrum_Expression import OCHIAI, TARANTULA, OP2
from xlsxwriter import Workbook


def summary_single_bugs():
    all_bugs_file_dir = join_path(EXPERIMENT_RESULT_FOLDER,
                                  "all_bugs.xlsx")
    file_lists = [
       "/Users/thu-trangnguyen/Documents/project/InputPreparation/experiment_results/DataV2_Results/BankAccountTP/ENABLE_NORMALIZATION/AGGREGATION_ARITHMETIC_MEAN/4wise/1Bug.xlsx",
        "/Users/thu-trangnguyen/Documents/project/InputPreparation/experiment_results/DataV2_Results/Elevator/ENABLE_NORMALIZATION/AGGREGATION_ARITHMETIC_MEAN/4wise/1Bug.xlsx",
        "/Users/thu-trangnguyen/Documents/project/InputPreparation/experiment_results/DataV2_Results/Email/ENABLE_NORMALIZATION/AGGREGATION_ARITHMETIC_MEAN/4wise/1Bug.xlsx",
        "/Users/thu-trangnguyen/Documents/project/InputPreparation/experiment_results/DataV2_Results/ExamDB/ENABLE_NORMALIZATION/AGGREGATION_ARITHMETIC_MEAN/4wise/1Bug.xlsx",
        "/Users/thu-trangnguyen/Documents/project/InputPreparation/experiment_results/DataV2_Results/GPL/ENABLE_NORMALIZATION/AGGREGATION_ARITHMETIC_MEAN/4wise/1Bug.xlsx",
        "/Users/thu-trangnguyen/Documents/project/InputPreparation/experiment_results/DataV2_Results/ZipMe/ENABLE_NORMALIZATION/AGGREGATION_ARITHMETIC_MEAN/4wise/1Bug.xlsx"

    ]
    write_all_bugs_to_a_file(all_bugs_file_dir, file_lists)

    summary_file = join_path(EXPERIMENT_RESULT_FOLDER,
                             "all_bugs_summary.xlsx")
    summary_result(all_bugs_file_dir, summary_file)
    hitx_file_dir = join_path(EXPERIMENT_RESULT_FOLDER,
                              "all_bugs_hix.xlsx")
    summary_hitx(hitx_file_dir, all_bugs_file_dir)

def summary_for_assumption_evaluation():

    all_bugs_file_dir = join_path(EXPERIMENT_RESULT_FOLDER,
                                      "all_assumption_all_bugs.xlsx")
    file_lists = [
        "/Users/thu-trangnguyen/Documents/project/InputPreparation/experiment_results/DataV2_Results/BankAccountTP/ENABLE_NORMALIZATION/AGGREGATION_ARITHMETIC_MEAN/4wise/1Bug.xlsx",
        "/Users/thu-trangnguyen/Documents/project/InputPreparation/experiment_results/DataV2_Results/Elevator/ENABLE_NORMALIZATION/AGGREGATION_ARITHMETIC_MEAN/4wise/1Bug.xlsx",
        "/Users/thu-trangnguyen/Documents/project/InputPreparation/experiment_results/DataV2_Results/Email/ENABLE_NORMALIZATION/AGGREGATION_ARITHMETIC_MEAN/4wise/1Bug.xlsx",
        "/Users/thu-trangnguyen/Documents/project/InputPreparation/experiment_results/DataV2_Results/ExamDB/ENABLE_NORMALIZATION/AGGREGATION_ARITHMETIC_MEAN/4wise/1Bug.xlsx",
        "/Users/thu-trangnguyen/Documents/project/InputPreparation/experiment_results/DataV2_Results/GPL/ENABLE_NORMALIZATION/AGGREGATION_ARITHMETIC_MEAN/4wise/1Bug.xlsx",
        "/Users/thu-trangnguyen/Documents/project/InputPreparation/experiment_results/DataV2_Results/ZipMe/ENABLE_NORMALIZATION/AGGREGATION_ARITHMETIC_MEAN/4wise/1Bug.xlsx"

    ]
    write_all_bugs_to_a_file(all_bugs_file_dir, file_lists)

    summary_file = join_path(EXPERIMENT_RESULT_FOLDER,
                             "all_assumption_summary.xlsx")
    assumption_summary_result(all_bugs_file_dir, summary_file)
    hitx_file_dir = join_path(EXPERIMENT_RESULT_FOLDER,
                              "all_assumption_hix.xlsx")
    assumption_summary_hitx(hitx_file_dir, all_bugs_file_dir)

def sbfl_only_summary_single_bugs():
    system = "new_all"
    all_bugs_file_dir = join_path(EXPERIMENT_RESULT_FOLDER,
                                  system + "single_bugs.xlsx")
    file_lists = [
        "/Users/thu-trangnguyen/Documents/project/InputPreparation/experiment_results/SBFL_ONLY/BankAccountTP/1Bug.xlsx",
        "/Users/thu-trangnguyen/Documents/project/InputPreparation/experiment_results/SBFL_ONLY/ExamDB/1Bug.xlsx",
        "/Users/thu-trangnguyen/Documents/project/InputPreparation/experiment_results/SBFL_ONLY/Elevator/1Bug.xlsx",
        "/Users/thu-trangnguyen/Documents/project/InputPreparation/experiment_results/SBFL_ONLY/GPL/1Bug.xlsx",
        "/Users/thu-trangnguyen/Documents/project/InputPreparation/experiment_results/SBFL_ONLY/Email/1Bug.xlsx",
        "/Users/thu-trangnguyen/Documents/project/InputPreparation/experiment_results/SBFL_ONLY/ZipMe/1Bug.xlsx",
    ]
    sbfl_only_write_all_bugs_to_a_file(all_bugs_file_dir, file_lists)

    summary_file = join_path(EXPERIMENT_RESULT_FOLDER,
                             system + "single_bug_rank_exam_new.xlsx")
    sbfl_only_summary_result(all_bugs_file_dir, summary_file)
    hitx_file_dir = join_path(EXPERIMENT_RESULT_FOLDER,
                              system + "_single_bug_top_n_new.xlsx")
    sbfl_only_summary_hitx(hitx_file_dir, all_bugs_file_dir)



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

def sbfl_only_summary_multiple_bugs():
    all_bugs_file_dir = join_path(EXPERIMENT_RESULT_FOLDER,
                                  "all3_only_multiple_bugs.xlsx")
    wb = Workbook(join_path(EXPERIMENT_RESULT_FOLDER,
                            "all_multiple_bugs3bug.xlsx"))
    file_lists = [
        "/Users/thu-trangnguyen/Documents/project/InputPreparation/experiment_results/SBFL_ONLY/ExamDB/3Bug.xlsx",
        "/Users/thu-trangnguyen/Documents/project/InputPreparation/experiment_results/SBFL_ONLY/Elevator/3Bug.xlsx",
        "/Users/thu-trangnguyen/Documents/project/InputPreparation/experiment_results/SBFL_ONLY/BankAccountTP/3Bug.xlsx",
        "/Users/thu-trangnguyen/Documents/project/InputPreparation/experiment_results/SBFL_ONLY/Email/3Bug.xlsx",
        "/Users/thu-trangnguyen/Documents/project/InputPreparation/experiment_results/SBFL_ONLY/GPL/3Bug.xlsx",
        "/Users/thu-trangnguyen/Documents/project/InputPreparation/experiment_results/SBFL_ONLY/ZipMe/3Bug.xlsx",


    ]
    sbfl_only_write_all_bugs_to_a_file(all_bugs_file_dir, file_lists)
    examined_statements = [1, 2, 3, 4, 5]
    #SPECTRUM_EXPRESSIONS_LIST
    for expression in SPECTRUM_EXPRESSIONS_LIST:
        row = 1
        sheet = wb.add_worksheet(expression)
        sbfl_only_write_headers(sheet)
        result_percentage_found_bugs_per_case = sbfl_only_percentage_of_bugs_found(all_bugs_file_dir, expression, examined_statements)
        sheet.write(row, 0, "PBL")
        for k in result_percentage_found_bugs_per_case.keys():
            sheet.write(row, 1, k)
            sheet.write(row, 2, result_percentage_found_bugs_per_case[k]['sbfl'])
            row += 1
        #print(result_percentage_found_bugs_per_case)hit

        result_percentages_of_cases_found_bugs = sbfl_only_num_of_case_found_bugs(all_bugs_file_dir, expression, examined_statements)
        sheet.write(row, 0, "Top-N")
        for k in result_percentages_of_cases_found_bugs.keys():
            sheet.write(row, 1, k)
            sheet.write(row, 2, result_percentages_of_cases_found_bugs[k]['hitx'])
            row += 1
        sheet.write(row, 0, "Proportion of cases that found bugs")
        for k in result_percentages_of_cases_found_bugs.keys():
            sheet.write(row, 1, k)
            sheet.write(row, 2, result_percentages_of_cases_found_bugs[k]['sbfl'])
            row += 1
        sheet.write(row, 0, "Best Rank")
        sheet.write(row, 2, sbfl_only_average_best_rank(all_bugs_file_dir, expression))
        row += 1
        sheet.write(row, 0, "Worst Rank")
        sheet.write(row, 2, sbfl_only_average_worst_rank(all_bugs_file_dir, expression))
        row += 1
        sheet.write(row, 0, "Best EXAM")
        sheet.write(row, 2, sbfl_only_average_best_exam(all_bugs_file_dir, expression))
        row += 1
        sheet.write(row, 0, "Worst EXAM")
        sheet.write(row, 2, sbfl_only_average_worst_exam(all_bugs_file_dir, expression))

        #print(result_percentages_of_cases_found_bugs)
    wb.close()


def sbfl_only_write_headers(sheet):
    sheet.write(0, 0, "EVALUATION_METRIC")
    sheet.write(0, 1, "NUM_OF_EXAMINED_STM")
    sheet.write(0, 2, "VALUE")
if __name__ == "__main__":

    #summary_single_bugs()
    summary_for_assumption_evaluation()
    #summary_multiple_bugs()
    #sbfl_only_summary_single_bugs()
    #sbfl_only_summary_multiple_bugs()




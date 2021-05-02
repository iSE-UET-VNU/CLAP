from experimental_results_analyzer.ExperimentalResultsAnalyzer import summary_result, summary_hitx, \
    write_all_bugs_to_a_file
from FileManager import join_path, EXPERIMENT_RESULT_FOLDER
from experimental_results_analyzer.ForAssumptionEvalutation_ExperimentalResultAnalyzer import assumption_summary_result, \
    assumption_summary_hitx


from xlsxwriter import Workbook


def summary_single_bugs():
    prefix = "temp1"

    systems = ["bank"]

    bank_file = ["BankAccountTP/ENABLE_NORMALIZATION/AGGREGATION_ARITHMETIC_MEAN/4wise/"]
    elevator = ["Elevator/ENABLE_NORMALIZATION/AGGREGATION_ARITHMETIC_MEAN/4wise/1Bug.xlsx"]
    email = ["Email/ENABLE_NORMALIZATION/AGGREGATION_ARITHMETIC_MEAN/4wise/1Bug.xlsx"]
    examdb = ["ExamDB/ENABLE_NORMALIZATION/AGGREGATION_ARITHMETIC_MEAN/4wise/1Bug.xlsx"]
    # gpl = ["GPL/ENABLE_NORMALIZATION/AGGREGATION_ARITHMETIC_MEAN/4wise/1Bug.xlsx"]
    # zipme = ["ZipMe/ENABLE_NORMALIZATION/AGGREGATION_ARITHMETIC_MEAN/4wise/1Bug.xlsx"]
    # file_lists = [
    #     bank_file[0], elevator[0], email[0], examdb[0], gpl[0], zipme[0]
    # ]
    experiments = [bank_file]
    num_of_bugs = ["1Bug", "2Bug", "3Bug"]
    base_path = join_path("/Users/thu-trangnguyen/Documents/project/InputPreparation/experiment_results/", prefix)
    for i in range(0, len(systems)):
        print(systems[i])
        all_bugs_file_dir = join_path(EXPERIMENT_RESULT_FOLDER,
                                      prefix + "_" + systems[i] + "temp.xlsx")

        #write_all_bugs_to_a_file(all_bugs_file_dir, experiments[i], num_of_bugs, base_path)

        summary_file = join_path(EXPERIMENT_RESULT_FOLDER,
                                 prefix + "_" + systems[i] + "_summary.xlsx")
        summary_result(all_bugs_file_dir, summary_file)
        # hitx_file_dir = join_path(EXPERIMENT_RESULT_FOLDER,
        #                           prefix + "_" + systems[i]+ "_hix.xlsx")
        # summary_hitx(hitx_file_dir, all_bugs_file_dir)


def summary_for_assumption_evaluation():
    prefix = "DataV2_NewRanking_1_0"

    systems = ["bank", "elevator", "email", "examdb", "gpl", "ZipMe", "all"]

    bank_file = ["BankAccountTP/ENABLE_NORMALIZATION/AGGREGATION_ARITHMETIC_MEAN/4wise/1Bug.xlsx"]
    elevator = ["Elevator/ENABLE_NORMALIZATION/AGGREGATION_ARITHMETIC_MEAN/4wise/1Bug.xlsx"]
    email = ["Email/ENABLE_NORMALIZATION/AGGREGATION_ARITHMETIC_MEAN/4wise/1Bug.xlsx"]
    examdb = ["ExamDB/ENABLE_NORMALIZATION/AGGREGATION_ARITHMETIC_MEAN/4wise/1Bug.xlsx"]
    gpl = ["GPL/ENABLE_NORMALIZATION/AGGREGATION_ARITHMETIC_MEAN/4wise/1Bug.xlsx"]
    zipme = ["ZipMe/ENABLE_NORMALIZATION/AGGREGATION_ARITHMETIC_MEAN/4wise/1Bug.xlsx"]
    file_lists = [
        bank_file[0], elevator[0], email[0], examdb[0], gpl[0], zipme[0]
    ]
    experiments = [bank_file, elevator, email, examdb, gpl, zipme, file_lists]
    base_path = join_path("/Users/thu-trangnguyen/Documents/project/InputPreparation/experiment_results/", prefix)
    for i in range(0, len(systems)):
        print(systems[i])
        all_bugs_file_dir = join_path(EXPERIMENT_RESULT_FOLDER,
                                      prefix + "_" + systems[i] + "_assumption_all_bugs.xlsx")

        write_all_bugs_to_a_file(all_bugs_file_dir, experiments[i], base_path)

        summary_file = join_path(EXPERIMENT_RESULT_FOLDER,
                                 prefix + "_" + systems[i] + "_summary.xlsx")
        assumption_summary_result(all_bugs_file_dir, summary_file)
        # hitx_file_dir = join_path(EXPERIMENT_RESULT_FOLDER,
        #                           prefix + "_" + systems[i]+ "_assumption_hix.xlsx")
        # assumption_summary_hitx(hitx_file_dir, all_bugs_file_dir)


# def summary_multiple_bugs():
#     all_bugs_file_dir = join_path(EXPERIMENT_RESULT_FOLDER,
#                                   "2021_0118_multiple_bugs.xlsx")
#     file_lists = [
#       "/Users/thu-trangnguyen/Documents/project/InputPreparation/experiment_results/public/multiple_bugs_AGGREGATION_ARITHMETIC_MEAN_NORMALIZATION_ALPHA_BETA/BankAccountTP/ranking_results.xlsx",
#       "/Users/thu-trangnguyen/Documents/project/InputPreparation/experiment_results/public/multiple_bugs_AGGREGATION_ARITHMETIC_MEAN_NORMALIZATION_ALPHA_BETA/BankAccountTP2new/ranking_results.xlsx",
#       "/Users/thu-trangnguyen/Documents/project/InputPreparation/experiment_results/public/multiple_bugs_AGGREGATION_ARITHMETIC_MEAN_NORMALIZATION_ALPHA_BETA/Elevator/ranking_results.xlsx"
#
#     ]
#     write_all_bugs_to_a_file(all_bugs_file_dir, file_lists)
#     examined_statements = [1, 2, 3, 4, 5,]
#     result_percentage_found_bugs = percentage_of_bugs_found(all_bugs_file_dir, OCHIAI, examined_statements)
#     print(result_percentage_found_bugs)
#     print("best", average_best_rank(all_bugs_file_dir, OCHIAI))
#     print("worst", average_worst_rank(all_bugs_file_dir, OCHIAI))
#     result_case_found_bugs = num_of_case_found_bugs(all_bugs_file_dir, OCHIAI, examined_statements)
#     print(result_case_found_bugs)


def sbfl_only_write_headers(sheet):
    sheet.write(0, 0, "EVALUATION_METRIC")
    sheet.write(0, 1, "NUM_OF_EXAMINED_STM")
    sheet.write(0, 2, "VALUE")


if __name__ == "__main__":
    summary_single_bugs()
    # summary_for_assumption_evaluation()
    # summary_multiple_bugs()
    # sbfl_only_summary_single_bugs()
    # sbfl_only_summary_multiple_bugs()

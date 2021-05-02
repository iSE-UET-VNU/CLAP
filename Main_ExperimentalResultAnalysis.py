import os

from experimental_results_analyzer.ExperimentalResultsAnalyzer import summary_result, summary_hitx, \
    write_all_bugs_to_a_file
from FileManager import join_path, EXPERIMENT_RESULT_FOLDER
from experimental_results_analyzer.ForAssumptionEvalutation_ExperimentalResultAnalyzer import assumption_summary_result, \
    assumption_summary_hitx


from xlsxwriter import Workbook

from experimental_results_analyzer.ImprovementComparisonAnalyzer import write_comparison_data_to_file


def summary_multiple_bugs():
    prefix = "DataV2_K0.5"

    systems = ["BankAccountTP", "Elevator", "Email", "ExamDB", "ALL"]

    bank_file = ["BankAccountTP/ENABLE_NORMALIZATION/AGGREGATION_ARITHMETIC_MEAN/4wise/"]
    elevator = ["Elevator/ENABLE_NORMALIZATION/AGGREGATION_ARITHMETIC_MEAN/4wise/"]
    email = ["Email/ENABLE_NORMALIZATION/AGGREGATION_ARITHMETIC_MEAN/4wise/"]
    examdb = ["ExamDB/ENABLE_NORMALIZATION/AGGREGATION_ARITHMETIC_MEAN/4wise/"]
    gpl = ["GPL/ENABLE_NORMALIZATION/AGGREGATION_ARITHMETIC_MEAN/4wise/"]
    # zipme = ["ZipMe/ENABLE_NORMALIZATION/AGGREGATION_ARITHMETIC_MEAN/4wise/"]
    file_lists = [
        bank_file[0], elevator[0], email[0], examdb[0]
    ]
    experiments = [bank_file]
    num_of_bugs = ["1Bug", "2Bug", "3Bug"]
    base_path = join_path("/Users/thu-trangnguyen/Documents/project/InputPreparation/experiment_results/", prefix)
    comparison_data = {}
    for i in range(0, len(systems)):
        print(systems[i])
        all_bugs_file_dir = join_path(EXPERIMENT_RESULT_FOLDER,
                                      prefix + "_" + systems[i] + "temp.xlsx")

        write_all_bugs_to_a_file(all_bugs_file_dir, experiments[i], num_of_bugs, base_path)

        summary_file = join_path(EXPERIMENT_RESULT_FOLDER,
                                 prefix + "_" + systems[i] + "_summary.xlsx")
        comparison_data[systems[i]] = summary_result(all_bugs_file_dir, summary_file, prefix + systems[i])
        comparison_file_path = join_path(EXPERIMENT_RESULT_FOLDER, prefix + "_comparison.xlsx")
        write_comparison_data_to_file(comparison_file_path, comparison_data)
        # hitx_file_dir = join_path(EXPERIMENT_RESULT_FOLDER,
        #                            prefix + "_" + systems[i]+ "_hix.xlsx")
        # summary_hitx(hitx_file_dir, all_bugs_file_dir, 5)
        os.remove(all_bugs_file_dir)

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




if __name__ == "__main__":
    summary_multiple_bugs()
    # summary_for_assumption_evaluation()

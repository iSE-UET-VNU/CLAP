import os

from experimental_results_analyzer.ExperimentalResultsAnalyzer import summary_result, summary_hitx, \
    write_all_bugs_to_a_file
from FileManager import join_path, EXPERIMENT_RESULT_FOLDER
from experimental_results_analyzer.ForAssumptionEvalutation_ExperimentalResultAnalyzer import write_all_bugs_to_a_file_for_assumption_evaluation

from xlsxwriter import Workbook

from experimental_results_analyzer.ImprovementComparisonAnalyzer import write_comparison_data_to_file


def summary_multiple_bugs():
    prefix = "DataV2_K0.5"

    systems = ["BankAccountTP", "Elevator", "Email", "ExamDB", "GPL", "ALL"]

    bank_file = ["BankAccountTP/ENABLE_NORMALIZATION/AGGREGATION_ARITHMETIC_MEAN/4wise/"]
    elevator = ["Elevator/ENABLE_NORMALIZATION/AGGREGATION_ARITHMETIC_MEAN/4wise/"]
    email = ["Email/ENABLE_NORMALIZATION/AGGREGATION_ARITHMETIC_MEAN/4wise/"]
    examdb = ["ExamDB/ENABLE_NORMALIZATION/AGGREGATION_ARITHMETIC_MEAN/4wise/"]
    gpl = ["GPL/ENABLE_NORMALIZATION/AGGREGATION_ARITHMETIC_MEAN/4wise/"]
    # zipme = ["ZipMe/ENABLE_NORMALIZATION/AGGREGATION_ARITHMETIC_MEAN/4wise/"]
    file_lists = [
        bank_file[0], elevator[0], email[0], examdb[0], gpl[0]
    ]
    experiments = [bank_file, elevator, email, examdb, gpl, file_lists]
    num_of_bugs = ["1Bug"]
    base_path = join_path("/Users/thu-trangnguyen/Documents/project/InputPreparation/experiment_results/", prefix)
    comparison_data = {}
    for i in range(0, len(systems)):
        print(systems[i])
        all_bugs_file_dir = join_path(EXPERIMENT_RESULT_FOLDER,
                                      prefix + "_" + systems[i] + "temp.xlsx")

        write_all_bugs_to_a_file(all_bugs_file_dir, experiments[i], num_of_bugs, base_path)

        summary_file = join_path(EXPERIMENT_RESULT_FOLDER,
                                 prefix + "_" + systems[i] + "_summary1bug.xlsx")
        comparison_data[systems[i]] = summary_result(all_bugs_file_dir, summary_file, prefix + systems[i])
        comparison_file_path = join_path(EXPERIMENT_RESULT_FOLDER, prefix + "_comparison1bug.xlsx")
        write_comparison_data_to_file(comparison_file_path, comparison_data)
        # hitx_file_dir = join_path(EXPERIMENT_RESULT_FOLDER,
        #                            prefix + "_" + systems[i]+ "_hix.xlsx")
        # summary_hitx(hitx_file_dir, all_bugs_file_dir, 5)
        os.remove(all_bugs_file_dir)


#only used to evaluate single bug
def summary_multiple_bugs_for_assumption_evaluation():
    prefix = "temp1"

    systems = ["BankAccountTP"]

    bank_file = ["BankAccountTP/ENABLE_NORMALIZATION/AGGREGATION_ARITHMETIC_MEAN/4wise/"]
    elevator = ["Elevator/ENABLE_NORMALIZATION/AGGREGATION_ARITHMETIC_MEAN/4wise/"]
    email = ["Email/ENABLE_NORMALIZATION/AGGREGATION_ARITHMETIC_MEAN/4wise/"]
    examdb = ["ExamDB/ENABLE_NORMALIZATION/AGGREGATION_ARITHMETIC_MEAN/4wise/"]
    gpl = ["GPL/ENABLE_NORMALIZATION/AGGREGATION_ARITHMETIC_MEAN/4wise/"]
    # zipme = ["ZipMe/ENABLE_NORMALIZATION/AGGREGATION_ARITHMETIC_MEAN/4wise/"]
    file_lists = [
        bank_file[0], elevator[0], email[0], examdb[0], gpl[0]
    ]
    experiments = [bank_file]
    num_of_bugs = ["1Bug"]
    base_path = join_path("/Users/thu-trangnguyen/Documents/project/InputPreparation/experiment_results/", prefix)
    comparison_data = {}
    for i in range(0, len(systems)):
        print(systems[i])
        all_bugs_file_dir = join_path(EXPERIMENT_RESULT_FOLDER,
                                      prefix + "_" + systems[i] + "temp.xlsx")

        write_all_bugs_to_a_file_for_assumption_evaluation(all_bugs_file_dir, experiments[i], num_of_bugs, base_path)

        #summary_file = join_path(EXPERIMENT_RESULT_FOLDER,
        #                         prefix + "_" + systems[i] + "_summary1bug.xlsx")
        #comparison_data[systems[i]] = summary_result(all_bugs_file_dir, summary_file, prefix + systems[i])
        #comparison_file_path = join_path(EXPERIMENT_RESULT_FOLDER, prefix + "_comparison1bug.xlsx")
        #write_comparison_data_to_file(comparison_file_path, comparison_data)
        # hitx_file_dir = join_path(EXPERIMENT_RESULT_FOLDER,
        #                            prefix + "_" + systems[i]+ "_hix.xlsx")
        # summary_hitx(hitx_file_dir, all_bugs_file_dir, 5)
        #os.remove(all_bugs_file_dir)




if __name__ == "__main__":
    #summary_multiple_bugs()
    summary_multiple_bugs_for_assumption_evaluation()

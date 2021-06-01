import os

from experimental_results_analyzer.ExperimentalResultsAnalyzer import summary_result, summary_hitx, \
    write_all_bugs_to_a_file, summary_percentage_bug_found
from FileManager import join_path, EXPERIMENT_RESULT_FOLDER
from experimental_results_analyzer.ForAssumptionEvalutation_ExperimentalResultAnalyzer import write_all_bugs_to_a_file_for_assumption_evaluation

from xlsxwriter import Workbook

from experimental_results_analyzer.ImprovementComparisonAnalyzer import write_comparison_data_to_file


def summary_multiple_bugs():
    prefix = "DataV2_2_0.5"

    systems = ["ALL"]

    bank_file = ["BankAccountTP/ENABLE_NORMALIZATION/AGGREGATION_ARITHMETIC_MEAN/4wise/"]
    elevator = ["Elevator/ENABLE_NORMALIZATION/AGGREGATION_ARITHMETIC_MEAN/4wise/"]
    email = ["Email/ENABLE_NORMALIZATION/AGGREGATION_ARITHMETIC_MEAN/4wise/"]
    examdb = ["ExamDB/ENABLE_NORMALIZATION/AGGREGATION_ARITHMETIC_MEAN/4wise/"]
    gpl = ["GPL/ENABLE_NORMALIZATION/AGGREGATION_ARITHMETIC_MEAN/4wise/"]
    zipme = ["ZipMe/ENABLE_NORMALIZATION/AGGREGATION_ARITHMETIC_MEAN/4wise/"]
    file_lists = [
        bank_file[0], elevator[0], email[0], examdb[0], gpl[0], zipme[0]
    ]
    experiments = [file_lists]
    num_of_bugs = ["2Bug", "3Bug"]
    base_path = join_path("/Users/thu-trangnguyen/Library/Mobile Documents/com~apple~CloudDocs/Documents/project/InputPreparation/experiment_results/", prefix)
    summary_path = join_path(base_path, "summary")
    if not os.path.exists(summary_path):
        os.makedirs(summary_path)
    comparison_data = {}
    for i in range(0, len(systems)):
        print(systems[i])
        all_bugs_file_dir = join_path(summary_path,
                                      prefix + "_" + systems[i] + "temp23.xlsx")

        #write_all_bugs_to_a_file(all_bugs_file_dir, experiments[i], num_of_bugs, base_path)

        # summary_file = join_path(summary_path,
        #                          prefix + "_" + systems[i] + "_summary23.xlsx")
        # comparison_data[systems[i]] = summary_result(all_bugs_file_dir, summary_file, prefix + systems[i])
        # comparison_file_path = join_path(summary_path, prefix + "_comparison23.xlsx")
        # write_comparison_data_to_file(comparison_file_path, comparison_data)
        # hitx_file_dir = join_path(summary_path,
        #                             prefix + "_" + systems[i]+ "_hix23.xlsx")
        # summary_hitx(hitx_file_dir, all_bugs_file_dir, 5)
        percentage_of_bug_found_file = join_path(summary_path,
                                                prefix + "_" + systems[i] + "percentage_of_bugs_found_op2.xlsx")
        summary_percentage_bug_found(all_bugs_file_dir, percentage_of_bug_found_file, prefix + systems[i])
        #os.remove(all_bugs_file_dir)


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
    summary_multiple_bugs()
    #summary_multiple_bugs_for_assumption_evaluation()

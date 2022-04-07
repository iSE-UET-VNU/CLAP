import os

from experimental_results_analyzer.ExperimentalResultsAnalyzer import summary_result, summary_hitx, \
    write_all_bugs_to_a_file, summary_percentage_of_cases_found_bugs, summary_pbl
from FileManager import join_path, EXPERIMENT_RESULT_FOLDER
from xlsxwriter import Workbook


def summary_multiple_bugs(num_of_bugs, base_path, prefix, experiments):
    summary_path = join_path(base_path, "summary")
    if not os.path.exists(summary_path):
        os.makedirs(summary_path)
    comparison_data = {}
    file_post_fix = ""
    for item in num_of_bugs:
        file_post_fix += item
    for i in range(0, len(systems)):
        print(systems[i])
        all_bugs_file_dir = join_path(summary_path,
                                      prefix + "_" + systems[i] + "temp" + file_post_fix + ".xlsx")

        write_all_bugs_to_a_file(all_bugs_file_dir, experiments[i], num_of_bugs, base_path)

        summary_file = join_path(summary_path,
                                 prefix + "_" + systems[i] + "_summary" + file_post_fix + ".xlsx")
        comparison_data[systems[i]] = summary_result(all_bugs_file_dir, summary_file, prefix + systems[i])
        # comparison_file_path = join_path(summary_path, prefix + "_comparison" + file_post_fix + ".xlsx")
        # #write_comparison_data_to_file(comparison_file_path, comparison_data)
        # hitx_file_dir = join_path(summary_path,
        #                           prefix + "_" + systems[i] + "_hix" + file_post_fix + ".xlsx")
        # summary_hitx(hitx_file_dir, all_bugs_file_dir, 5)
        # pbl_file = join_path(summary_path,
        #                      prefix + "_" + systems[i] + "plb" + file_post_fix + ".xlsx")
        # summary_pbl(all_bugs_file_dir, pbl_file, prefix + systems[i])
        # percentage_case_found_bug_file = join_path(summary_path,
        #                                            prefix + "_" + systems[
        #                                                i] + "percentage_case_found_bug_file" + file_post_fix + ".xlsx")
        # summary_percentage_of_cases_found_bugs(all_bugs_file_dir, percentage_case_found_bug_file, prefix + systems[i])
        os.remove(all_bugs_file_dir)


if __name__ == "__main__":
    num_of_bugs = ["1Bug", "2Bug", "3Bug"]
    prefix = "original"
    base_path = join_path("/home/huent/Documents/Project/CLAP/experiment_results", prefix)

    systems = [ "ALL"]

    bankaccount = ["BankAccountTP/ENABLE_NORMALIZATION/AGGREGATION_ARITHMETIC_MEAN/4wise/"]
    elevator = ["Elevator/ENABLE_NORMALIZATION/AGGREGATION_ARITHMETIC_MEAN/4wise/"]
    email = ["Email/ENABLE_NORMALIZATION/AGGREGATION_ARITHMETIC_MEAN/4wise/"]
    #examdb = ["ExamDB/ENABLE_NORMALIZATION/AGGREGATION_ARITHMETIC_MEAN/4wise/"]
    gpl = ["GPL/ENABLE_NORMALIZATION/AGGREGATION_ARITHMETIC_MEAN/1wise/"]
    zipme = ["ZipMe/ENABLE_NORMALIZATION/AGGREGATION_ARITHMETIC_MEAN/2wise/"]
    all = [
        bankaccount[0], elevator[0], email[0], gpl[0],
    ]
    experiments = [ all]
    summary_multiple_bugs(num_of_bugs, base_path, prefix, experiments)

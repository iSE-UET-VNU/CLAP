import os

from xlsxwriter import Workbook

from FileManager import join_path, list_dir, get_mutated_projects_dir, get_test_coverage_dir, get_all_variant_dirs, \
    EXPERIMENT_RESULT_FOLDER
from ranking.RankingManager import count_tests


def write_header_in_sumary_file(row, versions, sheet):
    sheet.write(row, 0, "system")
    sheet.write(row, 1, "kwise")
    sheet.write(row, 2, "mutated_project")
    sheet.write(row, 3, "variant")
    col = 4
    for version in versions:
        sheet.write(row, col, version)
        sheet.write(row + 1, col, "fails")
        sheet.write(row + 1, col + 1, "passes")
        col += 2



if __name__ == "__main__":

    base_dir = "/Users/thu-trangnguyen/Documents/Data/VarCop/"
    system_names = [ "Elevator"]
    kwises = ["4wise"]
    coverage_versions = ["", "INoT_1_", "INoT_2_", "INoT_3_", "INoT_4_", "INoT_5_", "INoT_6_", "INoT_7_", "INoT_8_", "INoT_9_", "INoT_10_"]

    base_path = join_path("/Users/thu-trangnguyen/Documents/project/InputPreparation/experiment_results/", "DataV2_NF_0.5")
    summary_path = join_path(base_path, "NumTests")
    if not os.path.exists(summary_path):
        os.makedirs(summary_path)
    summary_file_dir = join_path(summary_path,
                                 "Elevator2.xlsx")
    wb = Workbook(summary_file_dir)
    sheet = wb.add_worksheet("sheet1")

    row = 0
    write_header_in_sumary_file(row, coverage_versions, sheet)
    row += 2

    for system in system_names:
         sheet.write(row, 0, system)
         for k_wise in kwises:
             sheet.write(row, 1, k_wise)
             system_dir = join_path(join_path(base_dir, system), "1Bug")
             k_wise_dir = join_path(system_dir, k_wise)
             if os.path.isdir(k_wise_dir):
                 mutated_projects = list_dir(k_wise_dir)
                 for project in mutated_projects:
                     sheet.write(row, 2, project)
                     project_dir = join_path(k_wise_dir, project)
                     variants_list = get_all_variant_dirs(project_dir)
                     sum_test = {}
                     for version in coverage_versions:
                         sum_test[version] = 0
                     for variant_dir in variants_list:
                        #sheet.write(row, 3, variant_dir)

                        for version in coverage_versions:
                            test_coverage_dir = get_test_coverage_dir(variant_dir)
                            #fails, passes = count_tests(test_coverage_dir)
                            fails, passes = count_tests(test_coverage_dir, version)
                            #sheet.write(row, col, fails)
                            #sheet.write(row, col + 1, passes)
                            sum_test[version] += fails
                            sum_test[version] += passes
                            #col += 2
                        col = 4
                        for version in coverage_versions:
                            sheet.write(row, col, sum_test[version])
                            col += 2

                     row += 1
    wb.close()


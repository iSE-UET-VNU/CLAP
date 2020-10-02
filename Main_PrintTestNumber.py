import os

from xlsxwriter import Workbook

from FileManager import join_path, list_dir, get_mutated_projects_dir, get_test_coverage_dir, get_all_variants_dirs, \
    EXPERIMENT_RESULT_FOLDER
from RankingManager import count_tests, count_tests_original


def write_header_in_sumary_file(row, sheet):
    sheet.write(row, 1, "system")
    sheet.write(row, 2, "kwise")
    sheet.write(row, 3, "mutated_project")
    sheet.write(row, 4, "variant")
    sheet.write(row, 5, "fails")
    sheet.write(row, 6, "passes")

if __name__ == "__main__":

    base_dir = "/home/huent/Documents/Trang/"
    system_names = ["BankAccountTP", "Elevator", "Email", "ExamDB",  "GPL"]
    kwises = ["1wise", "2wise", "3wise", "4wise", "5wise"]

    summary_file_dir = join_path(EXPERIMENT_RESULT_FOLDER,
                                 "count_tests_v5.xlsx")
    wb = Workbook(summary_file_dir)
    sheet = wb.add_worksheet("sheet1")

    row = 0
    write_header_in_sumary_file(row, sheet)
    row += 1

    for system in system_names:
         sheet.write(row, 1, system)
         for k_wise in kwises:
             sheet.write(row, 2, k_wise)
             system_dir = join_path(base_dir, system)
             k_wise_dir = join_path(system_dir, k_wise)
             if os.path.isdir(k_wise_dir):
                 mutated_projects_dir = get_mutated_projects_dir(k_wise_dir)
                 mutated_projects = list_dir(mutated_projects_dir)
                 for project in mutated_projects:
                     sheet.write(row, 3, project)
                     project_dir = join_path(mutated_projects_dir, project)
                     variants_list = get_all_variants_dirs(project_dir)
                     for variant_dir in variants_list:
                        sheet.write(row, 4, variant_dir)
                        test_coverage_dir = get_test_coverage_dir(variant_dir)
                        #fails, passes = count_tests(test_coverage_dir)
                        fails, passes = count_tests(test_coverage_dir)
                        sheet.write(row, 5, fails)
                        sheet.write(row, 6, passes)
                        row += 1
    wb.close()


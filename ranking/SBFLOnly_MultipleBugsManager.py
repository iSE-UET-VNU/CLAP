import os

from xlsxwriter import Workbook

from ranking import RankingManager
from ranking.RankingManager import VARCOP_RANK, SBFL_RANK, \
    ranking_multiple_bugs, VARCOP_SPACE, SPACE, sbfl_only_ranking_multiple_bugs
from FileManager import join_path, EXPERIMENT_RESULT_FOLDER, get_mutated_projects_dir, list_dir, get_spc_log_file_path, \
    get_project_sub_dir_by_folder_name
from ranking.RankingResultManager import BUG_ID, BUGGY_STM, VARCOP_EXAM, SBFL_EXAM
from spc import SPCsManager
from suspicious_statements_manager import SlicingManager
from suspicious_statements_manager.SuspiciousStatementManager import get_multiple_buggy_statements, \
    get_suspicious_statement

BUG_ID_COL = 0
SBFL_BUGGY_STM_COL = 1
SBFL_RANK_COL = 2
SBFL_EXAM_COL = 3
SBFL_SPACE_COL = 4


def write_header_in_result_file(row, sheet):
    sheet.write(row, BUG_ID_COL, BUG_ID)
    sheet.write(row, SBFL_BUGGY_STM_COL, BUGGY_STM)
    sheet.write(row, SBFL_RANK_COL, SBFL_RANK)
    sheet.write(row, SBFL_EXAM_COL, SBFL_EXAM)
    sheet.write(row, SBFL_SPACE_COL, SPACE)


def write_result_to_file(row, sheet, ranking_results, space):
    temp = row

    for stm in ranking_results[SBFL_RANK]:
        sheet.write(temp, SBFL_BUGGY_STM_COL, stm)
        sheet.write(temp, SBFL_RANK_COL, ranking_results[SBFL_RANK][stm])
        sheet.write(temp, SBFL_EXAM_COL, (ranking_results[SBFL_RANK][stm] / space[SBFL_RANK]) * 100)
        sheet.write(temp, SBFL_SPACE_COL, space[SBFL_RANK])
        temp += 1
    row = temp
    return row


def sbfl_only_mutiple_bugs_ranking(result_folder, system_name, bug_folder, system_dir, spectrum_expressions, filtering_coverage_rate):
    mutated_projects_dir = ""
    print(list_dir(system_dir))
    for folder_name in list_dir(system_dir):
        mutated_projects_dir = get_project_sub_dir_by_folder_name(system_dir, folder_name)

    mutated_projects = list_dir(mutated_projects_dir)

    sheet = []

    row = 0
    search_rank_type_dir = join_path(EXPERIMENT_RESULT_FOLDER,
                                     result_folder)
    system_result_dir = join_path(search_rank_type_dir, system_name)
    if not os.path.exists(system_result_dir):
        os.makedirs(system_result_dir)
    experiment_file_name = join_path(system_result_dir, bug_folder + ".xlsx")

    wb = Workbook(experiment_file_name)

    for i in range(0, len(spectrum_expressions)):
        sheet.append(wb.add_worksheet(spectrum_expressions[i]))
        write_header_in_result_file(row, sheet[i])
    row += 1
    num_of_bugs = 0
    for mutated_project_name in mutated_projects:
        num_of_bugs += 1
        mutated_project_dir = join_path(mutated_projects_dir, mutated_project_name)
        buggy_statements = get_multiple_buggy_statements(mutated_project_name, mutated_project_dir)


        row_temp = row
        for sbfl_expression in range(0, len(spectrum_expressions)):
            ranking_results, space = sbfl_only_ranking_multiple_bugs(buggy_statements, mutated_project_dir,
                                                           spectrum_expressions[sbfl_expression],
                                                            coverage_rate=0.0)
            #
            sheet[sbfl_expression].write(row_temp, BUG_ID_COL, mutated_project_name)
            row = write_result_to_file(row_temp, sheet[sbfl_expression], ranking_results, space)

    wb.close()

import os

from xlsxwriter import Workbook

from ranking import RankingManager
from ranking.RankingManager import VARCOP_RANK, SBFL_RANK, \
    ranking_multiple_bugs, VARCOP_SPACE, SPACE
from FileManager import join_path, EXPERIMENT_RESULT_FOLDER, get_mutated_projects_dir, list_dir, get_spc_log_file_path
from ranking.RankingResultManager import BUG_ID, BUGGY_STM, VARCOP_EXAM, SBFL_EXAM
from spc import SPCsManager
from suspicious_statements_manager import SlicingManager
from suspicious_statements_manager.SuspiciousStatementManager import get_multiple_buggy_statements, \
    get_suspicious_statement

BUG_ID_COL = 0
VARCOP_BUGGY_STM_COL = 1
VARCOP_RANK_COL = 2
VARCOP_EXAM_COL = 3
VARCOP_SPACE_COL = 4
SBFL_BUGGY_STM_COL = 5
SBFL_RANK_COL = 6
SBFL_EXAM_COL = 7
SBFL_SPACE_COL = 8


def write_header_in_result_file(row, sheet):
    sheet.write(row, BUG_ID_COL, BUG_ID)
    sheet.write(row, VARCOP_BUGGY_STM_COL, BUGGY_STM)
    sheet.write(row, VARCOP_RANK_COL, VARCOP_RANK)
    sheet.write(row, VARCOP_EXAM_COL, VARCOP_EXAM)
    sheet.write(row, VARCOP_SPACE_COL, VARCOP_SPACE)
    sheet.write(row, SBFL_BUGGY_STM_COL, BUGGY_STM)
    sheet.write(row, SBFL_RANK_COL, SBFL_RANK)
    sheet.write(row, SBFL_EXAM_COL, SBFL_EXAM)
    sheet.write(row, SBFL_SPACE_COL, SPACE)


def write_result_to_file(row, sheet, ranking_results, space):
    temp = row

    for stm in ranking_results[VARCOP_RANK].keys():
        sheet.write(temp, VARCOP_BUGGY_STM_COL, stm)
        sheet.write(temp, VARCOP_RANK_COL, ranking_results[VARCOP_RANK][stm])
        for sbfl_stm in ranking_results[SBFL_RANK]:
            if stm == sbfl_stm:
                print(type(ranking_results[VARCOP_RANK][stm]))
                print(type(space[SBFL_RANK]))
                exam = (ranking_results[VARCOP_RANK][stm] / space[SBFL_RANK]) * 100
                sheet.write(temp, VARCOP_EXAM_COL, exam)
                break
        sheet.write(temp, VARCOP_SPACE_COL, space[VARCOP_RANK])
        temp += 1

    temp = row
    for stm in ranking_results[SBFL_RANK]:
        sheet.write(temp, SBFL_BUGGY_STM_COL, stm)
        sheet.write(temp, SBFL_RANK_COL, ranking_results[SBFL_RANK][stm])
        sheet.write(temp, SBFL_EXAM_COL, (ranking_results[SBFL_RANK][stm] / space[SBFL_RANK]) * 100)
        sheet.write(temp, SBFL_SPACE_COL, space[SBFL_RANK])
        temp += 1
    row = temp
    return row


def mutiple_bugs_ranking(result_folder, system_name, system_dir, spectrum_expressions, filtering_coverage_rate):
    aggregations = [RankingManager.AGGREGATION_ARITHMETIC_MEAN]
    normalizations = [RankingManager.NORMALIZATION_ALPHA_BETA]
    mutated_projects_dir = get_mutated_projects_dir(system_dir)
    mutated_projects = list_dir(mutated_projects_dir)
    for aggregation_type in aggregations:
        for normalization_type in normalizations:
            sheet = []

            row = 0
            search_rank_type_dir = join_path(EXPERIMENT_RESULT_FOLDER,
                                             result_folder + str(aggregation_type)) + "_" + str(normalization_type)
            system_result_dir = join_path(search_rank_type_dir, system_name)
            if not os.path.exists(system_result_dir):
                os.makedirs(system_result_dir)
            experiment_file_name = join_path(system_result_dir,
                                             str(filtering_coverage_rate) + "_" + ".xlsx")

            wb = Workbook(experiment_file_name)

            for i in range(0, len(spectrum_expressions)):
                sheet.append(wb.add_worksheet(spectrum_expressions[i]))
                write_header_in_result_file(row, sheet[i])
            row += 1
            num_of_bugs = 0
            for mutated_project_name in mutated_projects:
                num_of_bugs += 1
                mutated_project_dir = join_path(mutated_projects_dir, mutated_project_name)
                # spc_log_file_path = SPCsManager.find_SPCs(mutated_project_dir, filtering_coverage_rate)

                # spc_log_file_path = get_spc_log_file_path(mutated_project_dir, filtering_coverage_rate)
                # SlicingManager.do_slice(spc_log_file_path, filtering_coverage_rate, "")
                suspicious_stms_list = get_suspicious_statement(mutated_project_dir, filtering_coverage_rate)
                buggy_statements = get_multiple_buggy_statements(mutated_project_name, mutated_project_dir)
                # print(buggy_statements)
                #

                row_temp = row
                for sbfl_expression in range(0, len(spectrum_expressions)):
                    ranking_results, space = ranking_multiple_bugs(buggy_statements, mutated_project_dir,
                                                                   suspicious_stms_list,
                                                                   spectrum_expressions[sbfl_expression],
                                                                   aggregation_type,
                                                                   normalization_type, coverage_rate=0.0)
                    #
                    sheet[sbfl_expression].write(row_temp, BUG_ID_COL, mutated_project_name)
                    row = write_result_to_file(row_temp, sheet[sbfl_expression], ranking_results, space)

            wb.close()

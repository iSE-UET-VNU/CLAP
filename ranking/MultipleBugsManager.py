import os

from xlsxwriter import Workbook

from ranking import RankingManager
from ranking.FeaturesRankingManager import features_ranking_multiple_bugs
from ranking.Keywords import VARCOP_DISABLE_BPC_RANK, VARCOP_DISABLE_BPC_EXAM, FB_RANK, FB_EXAM
from ranking.RankingManager import VARCOP_RANK, SBFL_RANK, \
    ranking_multiple_bugs, VARCOP_SPACE, SPACE
from FileManager import join_path, EXPERIMENT_RESULT_FOLDER, get_mutated_projects_dir, list_dir, get_spc_log_file_path, \
    get_project_sub_dir_by_folder_name
from ranking.RankingResultManager import BUG_ID, BUGGY_STM, VARCOP_EXAM, SBFL_EXAM, write_runtime_to_file
from spc import SPCsManager
from suspicious_statements_manager import SlicingManager
from suspicious_statements_manager.SuspiciousStatementManager import get_multiple_buggy_statements, \
    get_suspicious_statement

BUG_ID_COL = 0
VARCOP_BUGGY_STM_COL = 1
VARCOP_RANK_COL = 2
VARCOP_EXAM_COL = 3
VARCOP_SPACE_COL = 4
VARCOP_DISABLE_BPC_RANK_COL = 5
VARCOP_DISABLE_BPC_EXAM_COL = 6
SBFL_RANK_COL = 7
SBFL_EXAM_COL = 8
FB_RANK_COL = 9
FB_EXAM_COL = 10
SBFL_SPACE_COL = 11


def write_header_in_result_file(row, sheet):
    sheet.write(row, BUG_ID_COL, BUG_ID)
    sheet.write(row, VARCOP_BUGGY_STM_COL, BUGGY_STM)
    sheet.write(row, VARCOP_RANK_COL, VARCOP_RANK)
    sheet.write(row, VARCOP_EXAM_COL, VARCOP_EXAM)
    sheet.write(row, VARCOP_SPACE_COL, VARCOP_SPACE)
    sheet.write(row, VARCOP_DISABLE_BPC_RANK_COL, VARCOP_DISABLE_BPC_RANK)
    sheet.write(row, VARCOP_DISABLE_BPC_EXAM_COL, VARCOP_DISABLE_BPC_EXAM)
    sheet.write(row, SBFL_RANK_COL, SBFL_RANK)
    sheet.write(row, SBFL_EXAM_COL, SBFL_EXAM)
    sheet.write(row, FB_RANK_COL, FB_RANK)
    sheet.write(row, FB_EXAM_COL, FB_EXAM)
    sheet.write(row, SBFL_SPACE_COL, SPACE)


def write_result_to_file(row, sheet, ranking_results, space):

    for stm in ranking_results[VARCOP_RANK].keys():
        sheet.write(row, VARCOP_BUGGY_STM_COL, stm)
        sheet.write(row, VARCOP_RANK_COL, ranking_results[VARCOP_RANK][stm])
        exam = (ranking_results[VARCOP_RANK][stm] / space[SBFL_RANK]) * 100
        sheet.write(row, VARCOP_EXAM_COL, exam)
        sheet.write(row, VARCOP_SPACE_COL, space[VARCOP_RANK])

        sheet.write(row, VARCOP_DISABLE_BPC_RANK_COL, ranking_results[VARCOP_DISABLE_BPC_RANK][stm])
        disabled_bpc_exam = (ranking_results[VARCOP_DISABLE_BPC_RANK][stm] / space[SBFL_RANK]) * 100
        sheet.write(row, VARCOP_DISABLE_BPC_EXAM_COL, disabled_bpc_exam)

        sheet.write(row, SBFL_RANK_COL, ranking_results[SBFL_RANK][stm])
        sheet.write(row, SBFL_EXAM_COL, (ranking_results[SBFL_RANK][stm] / space[SBFL_RANK]) * 100)

        sheet.write(row, FB_RANK_COL, ranking_results[FB_RANK][stm])
        sheet.write(row, FB_EXAM_COL, (ranking_results[FB_RANK][stm] / space[SBFL_RANK]) * 100)

        sheet.write(row, SBFL_SPACE_COL, space[SBFL_RANK])
        row += 1
    return row


def mutiple_bugs_ranking(result_folder, system_name, bug_folder, system_dir, spectrum_expressions, filtering_coverage_rate, alpha):
    aggregations = [RankingManager.AGGREGATION_ARITHMETIC_MEAN]
    normalizations = [RankingManager.NORMALIZATION_ALPHA_BETA]
    mutated_projects_dir = ""
    for folder_name in list_dir(system_dir):
        mutated_projects_dir = get_project_sub_dir_by_folder_name(system_dir, folder_name)
    mutated_projects = list_dir(mutated_projects_dir)

    result_folder_dir = join_path(EXPERIMENT_RESULT_FOLDER, result_folder)
    if not os.path.exists(result_folder_dir):
        os.makedirs(result_folder_dir)

    system_result_dir = join_path(result_folder_dir, system_name)
    if not os.path.exists(system_result_dir):
        os.makedirs(system_result_dir)


    for normalization_type in normalizations:
        normalization_result_dir = join_path(system_result_dir, normalization_type)
        if not os.path.exists(normalization_result_dir):
            os.makedirs(normalization_result_dir)

        for aggregation_type in aggregations:
            aggregation_result_dir = join_path(normalization_result_dir, aggregation_type)
            if not os.path.exists(aggregation_result_dir):
                os.makedirs(aggregation_result_dir)

            kwise_result_dir = join_path(aggregation_result_dir, "4wise")
            if not os.path.exists(kwise_result_dir):
                os.makedirs(kwise_result_dir)

            sheet = []

            row = 0

            experiment_file_name = join_path(kwise_result_dir,
                                             bug_folder + ".xlsx")
            if os.path.exists(experiment_file_name):
                continue
            wb = Workbook(experiment_file_name)

            for i in range(0, len(spectrum_expressions)):
                sheet.append(wb.add_worksheet(spectrum_expressions[i]))
                write_header_in_result_file(row, sheet[i])
            row += 1
            num_of_bugs = 0
            runtime = {}
            for mutated_project_name in mutated_projects:
                num_of_bugs += 1
                mutated_project_dir = join_path(mutated_projects_dir, mutated_project_name)
                #spc_log_file_path, spc_runtime = SPCsManager.find_SPCs(mutated_project_dir, filtering_coverage_rate)

                #spc_log_file_path = get_spc_log_file_path(mutated_project_dir, filtering_coverage_rate)
                #slicing_runtime = SlicingManager.do_slice(spc_log_file_path, filtering_coverage_rate, "")
                suspicious_stms_list = get_suspicious_statement(mutated_project_dir, filtering_coverage_rate)
                buggy_statements = get_multiple_buggy_statements(mutated_project_name, mutated_project_dir)
                # print(buggy_statements)
                #

                row_temp = row
                varcop_ranking_time = 0
                for sbfl_expression in range(0, len(spectrum_expressions)):
                    ranking_results, space, varcop_ranking_time = ranking_multiple_bugs(buggy_statements, mutated_project_dir,
                                                                   suspicious_stms_list,
                                                                   spectrum_expressions[sbfl_expression],
                                                                   aggregation_type,
                                                                   normalization_type, "", filtering_coverage_rate, alpha)
                    ranking_results[FB_RANK] = features_ranking_multiple_bugs(buggy_statements, mutated_project_dir,
                                                            filtering_coverage_rate, spectrum_expressions[sbfl_expression])
                    #
                    sheet[sbfl_expression].write(row_temp, BUG_ID_COL, mutated_project_name)
                    row = write_result_to_file(row_temp, sheet[sbfl_expression], ranking_results, space)
                #runtime[mutated_project_name] = [spc_runtime, slicing_runtime, varcop_ranking_time]
            #write_runtime_to_file(system_result_dir, runtime, "multiple_bug_runtime.xlsx")

            wb.close()

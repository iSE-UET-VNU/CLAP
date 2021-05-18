import logging
import os

from spc import SPCsManager
from suspicious_statements_manager import SlicingManager
from ranking.FeaturesRankingManager import features_ranking
from FileManager import get_project_dir, get_mutated_projects_dir, join_path, EXPERIMENT_RESULT_FOLDER, list_dir, \
    get_spc_log_file_path
import MutantManager
from ranking import RankingManager
from ranking.Keywords import *

from suspicious_statements_manager.SuspiciousStatementManager import get_suspicious_statement, get_buggy_statement, \
    get_single_buggy_statement
from xlsxwriter import Workbook

BUG_ID_COL = 0
BUGGY_STM_COL = 1
VARCOP_RANK_COL = 2
VARCOP_EXAM_COL = 3
VARCOP_SPACE_COL = 4
VARCOP_DISABLE_BPC_RANK_COL = 5
VARCOP_DISABLE_BPC_EXAM_COL = 6
SBFL_RANK_COL = 7
SBFL_EXAM_COL = 8
FB_RANK_COL = 9
FB_EXAM_COL = 10
SPACE_COL = 11



def write_header_in_result_file(row, sheet):
    sheet.write(row, BUG_ID_COL, BUG_ID)
    sheet.write(row, BUGGY_STM_COL, BUGGY_STM)
    sheet.write(row, VARCOP_RANK_COL, VARCOP_RANK)
    sheet.write(row, VARCOP_EXAM_COL, VARCOP_EXAM)
    sheet.write(row, VARCOP_SPACE_COL, VARCOP_SPACE)
    sheet.write(row, VARCOP_DISABLE_BPC_RANK_COL, VARCOP_DISABLE_BPC_RANK)
    sheet.write(row, VARCOP_DISABLE_BPC_EXAM_COL, VARCOP_DISABLE_BPC_EXAM)
    sheet.write(row, SBFL_RANK_COL, SBFL_RANK)
    sheet.write(row, SBFL_EXAM_COL, SBFL_EXAM)
    sheet.write(row, FB_RANK_COL, FB_RANK)
    sheet.write(row, FB_EXAM_COL, FB_EXAM)
    sheet.write(row, SPACE_COL, SPACE)


def write_results_to_file(row, sheet, ranking_results):
    varcop_rank = ranking_results[VARCOP_RANK]
    sheet.write(row, VARCOP_RANK_COL, varcop_rank)

    varcop_exam = (ranking_results[VARCOP_RANK] / ranking_results[SPACE]) * 100
    sheet.write(row, VARCOP_EXAM_COL, varcop_exam)

    varcop_space = ranking_results[VARCOP_SPACE]
    sheet.write(row, VARCOP_SPACE_COL, varcop_space)

    varcop_disable_bpc_rank = ranking_results[VARCOP_DISABLE_BPC_RANK]
    sheet.write(row, VARCOP_DISABLE_BPC_RANK_COL, varcop_disable_bpc_rank)

    varcop_disable_exam = (ranking_results[VARCOP_DISABLE_BPC_RANK] / ranking_results[SPACE]) * 100
    sheet.write(row, VARCOP_DISABLE_BPC_EXAM_COL, varcop_disable_exam)

    sbfl_rank = ranking_results[SBFL_RANK]
    sheet.write(row, SBFL_RANK_COL, sbfl_rank)

    sbfl_exam = (ranking_results[SBFL_RANK] / ranking_results[SPACE]) * 100
    sheet.write(row, SBFL_EXAM_COL, sbfl_exam)

    fb_rank = ranking_results[FB_RANK]
    sheet.write(row, FB_RANK_COL, fb_rank)

    fb_exam = (ranking_results[FB_RANK] / ranking_results[SPACE]) * 100
    sheet.write(row, FB_EXAM_COL, fb_exam)

    space = ranking_results[SPACE]
    sheet.write(row, SPACE_COL, space)
    row += 1

    return row


def ranking_with_coverage_rate(result_folder, base_dir, system, project_name, filtering_coverage_rate,
                               spectrum_expressions, spectrum_coverage_prefix):
    # aggregations = [ RankingManager.AGGREGATION_GEOMETRIC_MEAN,
    #                 RankingManager.AGGREGATION_MEDIAN, RankingManager.AGGREGATION_MAX, RankingManager.AGGREGATION_MIN, RankingManager.AGGREGATION_MODE]

    normalizations = [RankingManager.NORMALIZATION_ALPHA_BETA]
    aggregations = [RankingManager.AGGREGATION_ARITHMETIC_MEAN]
    result_folder_dir = join_path(EXPERIMENT_RESULT_FOLDER, result_folder)
    if not os.path.exists(result_folder_dir):
        os.makedirs(result_folder_dir)

    system_result_dir = join_path(result_folder_dir, system)
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

            sheet = []
            project_dir = get_project_dir(project_name, base_dir)
            row = 0

            project_result_dir = join_path(aggregation_result_dir, project_name)
            if not os.path.exists(project_result_dir):
                os.makedirs(project_result_dir)
            experiment_file_name = join_path(project_result_dir,
                                              "1Bug.xlsx")
            wb = Workbook(experiment_file_name)

            for i in range(0, len(spectrum_expressions)):
                sheet.append(wb.add_worksheet(spectrum_expressions[i]))
                write_header_in_result_file(row, sheet[i])

            row += 1
            mutated_projects_dir = get_mutated_projects_dir(project_dir)
            mutated_projects = list_dir(mutated_projects_dir)
            runtime = {}
            for mutated_project_name in mutated_projects:

                # try:
                ranking_project = project_name + "_" + mutated_project_name

                logging.info("Ranking... %s", ranking_project)

                mutated_project_dir = MutantManager.get_mutated_project_dir(project_dir, mutated_project_name)

                spc_log_file_path, spc_runtime = SPCsManager.find_SPCs(mutated_project_dir, filtering_coverage_rate)
                spc_log_file_path = get_spc_log_file_path(mutated_project_dir, filtering_coverage_rate)
                # print(spc_log_file_path)
                slicing_runtime = SlicingManager.do_slice_spc(spc_log_file_path, filtering_coverage_rate, spectrum_coverage_prefix)
                if spectrum_coverage_prefix != "":
                    post_fix = str(filtering_coverage_rate) + "_" + spectrum_coverage_prefix + "_"
                else:
                    post_fix = filtering_coverage_rate

                suspicious_stms_list = get_suspicious_statement(mutated_project_dir, post_fix)

                buggy_statement = get_single_buggy_statement(mutated_project_name, mutated_project_dir)
                row_temp = row
                varcop_ranking_time = 0
                for i in range(0, len(spectrum_expressions)):
                    ranking_results, varcop_ranking_time = RankingManager.ranking(system, buggy_statement, mutated_project_dir,
                                                             suspicious_stms_list, spectrum_expressions[i],
                                                             aggregation_type, normalization_type,
                                                             spectrum_coverage_prefix, filtering_coverage_rate)

                    ranking_results["feature_rank"], ranking_results[FB_RANK], ranking_results[
                        "feature_space"] = features_ranking(buggy_statement, mutated_project_dir,
                                                            filtering_coverage_rate, spectrum_expressions[i],
                                                            spectrum_coverage_prefix)

                    sheet[i].write(row_temp, BUG_ID_COL, mutated_project_name)
                    sheet[i].write(row_temp, BUGGY_STM_COL, buggy_statement)
                    row = write_results_to_file(row_temp, sheet[i], ranking_results)
                runtime[mutated_project_name] = [spc_runtime, slicing_runtime, varcop_ranking_time]
            write_runtime_to_file(system_result_dir, runtime, "single_bug_runtime.xlsx")
            wb.close()


def write_runtime_to_file(system_result_dir, run_time, file_name):
    experiment_file_name = join_path(system_result_dir,
                                     file_name)
    if os.path.exists(experiment_file_name):
        return
    wb = Workbook(experiment_file_name)
    sheet = wb.add_worksheet("run_time")
    row = 0
    for item in run_time.keys():
        sheet.write(row, 0, item)
        col = 1
        for time in run_time[item]:
            sheet.write(row, col, time)
            col += 1
        row += 1
    wb.close()

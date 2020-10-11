import logging
import os
import time

import SPCsManager
import SlicingManager
from FeaturesRankingManager import features_ranking
from FileManager import get_project_dir, get_mutated_projects_dir, join_path, EXPERIMENT_RESULT_FOLDER, list_dir
import MutantManager
import RankingManager
from RankingManager import  VARCOP_SPC_FAILING, VARCOP_SPC_SEARCH_SPACE, SPECTRUM, SPECTRUM_SEARCH_SPACE, VARCOP_SPC_LAYER, VARCOP_FAILING, VARCOP_LAYER, VARCOP_SEARCH_SPACE

from SuspiciousStatementManager import get_suspicious_statement, get_buggy_statement
from xlsxwriter import Workbook


MUTATED_PROJECT_COL = 0

VARCOP_SPC_FAILING_COL = 1
VARCOP_SPC_LAYER_COL = 2
VARCOP_SPC_SPACE_COL = 3
VARCOP_FAILING_COL = 4
VARCOP_LAYER_COL = 5
VARCOP_SPACE_COL = 6
SPECTRUM_COL = 7
SPECTRUM_SPACE_COL = 8
FEATURE_COL = 9
FEATURE_STM_COL = 10
FEATURE_SPACE_COL = 11

SYSTEM_HEADER = "SYSTEM"
K_WISE_HEADER = "K_WISE"
MUTATED_PROJECT_HEADER = "MUTATED_PROJECT"
VARCOP_SPC_FAILING_HEADER = "SPC_FAILING_ONLY"
VARCOP_SPC_LAYER_HEADER = "SPC_LAYER"
VARCOP_SPC_SPACE_HEADER = "SPC_SPACE"
VARCOP_FAILING_HEADER = "WITHOUT_ISOLATION_F"
VARCOP_LAYER_HEADER = "WITHOUT_ISOLATION_LAYER"
VARCOP_SPACE_HEADER = "WITHOUT_ISOLATION_SPACE"
SPECTRUM_HEADER = "SPECTRUM"
SPECTRUM_SPACE_HEADER = "SPECTRUM_SPACE"
FEATURE_HEADER = "FEATURE"
FEATURE_STM_HEADER = "FEATURE_STM"
FEATURE_SPACE_HEADER = "FEATURE_SPACE"

FEATURE_RANK = "feature_rank"
FEATURE_STM_RANK = "feature_stm_rank"
FEATURE_SPACE = "feature_space"


def write_header_in_result_file(row, sheet):
    sheet.write(row, MUTATED_PROJECT_COL, MUTATED_PROJECT_HEADER)
    sheet.write(row, VARCOP_SPC_FAILING_COL, VARCOP_SPC_FAILING_HEADER)
    sheet.write(row, VARCOP_SPC_LAYER_COL, VARCOP_SPC_LAYER_HEADER)
    sheet.write(row, VARCOP_SPC_SPACE_COL, VARCOP_SPC_SPACE_HEADER)
    sheet.write(row, VARCOP_FAILING_COL, VARCOP_FAILING_HEADER)
    sheet.write(row, VARCOP_LAYER_COL, VARCOP_LAYER_HEADER)
    sheet.write(row, VARCOP_SPACE_COL, VARCOP_SPACE_HEADER)
    sheet.write(row, SPECTRUM_COL, SPECTRUM_HEADER)
    sheet.write(row, SPECTRUM_SPACE_COL, SPECTRUM_SPACE_HEADER)
    sheet.write(row, FEATURE_COL, FEATURE_HEADER)
    sheet.write(row, FEATURE_STM_COL, FEATURE_STM_HEADER)
    sheet.write(row, FEATURE_SPACE_COL, FEATURE_SPACE_HEADER)


def write_results_to_file(row, sheet, ranking_results):

    spc_spectrum_rank1 = ranking_results[VARCOP_SPC_FAILING]
    sheet.write(row, VARCOP_SPC_FAILING_COL, spc_spectrum_rank1)

    spc_layer_rank = ranking_results[VARCOP_SPC_LAYER]
    sheet.write(row, VARCOP_SPC_LAYER_COL, spc_layer_rank)

    spc_space = ranking_results[VARCOP_SPC_SEARCH_SPACE]
    sheet.write(row, VARCOP_SPC_SPACE_COL, spc_space)

    without_isolation_F = ranking_results[VARCOP_FAILING]
    sheet.write(row, VARCOP_FAILING_COL, without_isolation_F)

    without_isolation_layer = ranking_results[VARCOP_LAYER]
    sheet.write(row, VARCOP_LAYER_COL, without_isolation_layer)

    without_isolation_space = ranking_results[VARCOP_SEARCH_SPACE]
    sheet.write(row, VARCOP_SPACE_COL, without_isolation_space)

    spectrum_rank = ranking_results[SPECTRUM]
    sheet.write(row, SPECTRUM_COL, spectrum_rank)

    spectrum_space = ranking_results[SPECTRUM_SEARCH_SPACE]
    sheet.write(row, SPECTRUM_SPACE_COL, spectrum_space)

    feature_rank = ranking_results[FEATURE_RANK]
    sheet.write(row, FEATURE_COL, feature_rank)

    feature_stm_rank = ranking_results[FEATURE_STM_RANK]
    sheet.write(row, FEATURE_STM_COL, feature_stm_rank)

    feature_space = ranking_results[FEATURE_SPACE]
    sheet.write(row, FEATURE_SPACE_COL, feature_space)
    row += 1

    return row


def ranking_with_coverage_rate(base_dir, system, project_name, filtering_coverage_rate, spectrum_expressions, spectrum_coverage_prefix):

    score_aggregations = [RankingManager.AGGREATION_PRODUCT_RELATED, RankingManager.AGGREATION_ALL_PRODUCT]
    result_folder = "test"
    for t in score_aggregations:
        sheet = []
        project_dir = get_project_dir(project_name, base_dir)
        row = 0
        search_rank_type_dir = join_path(EXPERIMENT_RESULT_FOLDER, result_folder + str(t))
        system_result_dir = join_path(search_rank_type_dir, system)
        if not os.path.exists(system_result_dir):
            os.makedirs(system_result_dir)
        project_result_dir = join_path(system_result_dir, project_name)
        if not os.path.exists(project_result_dir):
            os.makedirs(project_result_dir)
        experiment_file_name = join_path(project_result_dir,
                                         str(filtering_coverage_rate)+ "_" + ".xlsx")
        wb = Workbook(experiment_file_name)

        for i in range(0, len(spectrum_expressions)):
            sheet.append(wb.add_worksheet(spectrum_expressions[i]))
            write_header_in_result_file(row, sheet[i])

        row += 1
        mutated_projects_dir = get_mutated_projects_dir(project_dir)
        mutated_projects = list_dir(mutated_projects_dir)

        for mutated_project_name in mutated_projects:
            # try:
            ranking_project = project_name + "_" + mutated_project_name

            logging.info("Ranking... %s", ranking_project)

            mutated_project_dir = MutantManager.get_mutated_project_dir(project_dir, mutated_project_name)

            #spc_log_file_path = SPCsManager.find_SPCs(mutated_project_dir, filtering_coverage_rate)

            #SlicingManager.do_slice(spc_log_file_path, filtering_coverage_rate)
            suspicious_stms_list = get_suspicious_statement(mutated_project_dir, filtering_coverage_rate)

            buggy_statement = get_buggy_statement(mutated_project_name, mutated_project_dir)

            row_temp = row
            for i in range(0, len(spectrum_expressions)):
                ranking_results = RankingManager.ranking(buggy_statement, mutated_project_dir,
                                                         suspicious_stms_list, spectrum_expressions[i], t, spectrum_coverage_prefix)

                ranking_results[FEATURE_RANK], ranking_results[FEATURE_STM_RANK], ranking_results[FEATURE_SPACE] = features_ranking(buggy_statement, mutated_project_dir, suspicious_stms_list.keys(), filtering_coverage_rate, spectrum_expressions[i], spectrum_coverage_prefix)
                sheet[i].write(row_temp, MUTATED_PROJECT_COL, mutated_project_name)
                row = write_results_to_file(row_temp, sheet[i], ranking_results)

        # except:
        #   logging.info(" Exception in ranking %s", mutated_project_name)

        wb.close()

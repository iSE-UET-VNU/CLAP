import logging
import os

import SPCsManager
import SlicingManager
from FileManager import get_project_dir, get_mutated_projects_dir, join_path, EXPERIMENT_RESULT_FOLDER, \
    SPC_LOG_FILE_NAME, list_dir
import MutantManager
import RankingManager
from SuspiciousStatementManager import get_suspicious_statement, get_buggy_statement
import threading
from xlsxwriter import Workbook
import multiprocessing

MUTATED_PROJECT_COL = 0
VARIANT_COL = 1
SPECTRUM_COL = 2
SPECTRUM_SPACE_COL = 3
SPECTRUM_DETAIL_COL = 4
SPC_SPECTRUM_COL = 5
SPC_SPECTRUM_SPACE_COL = 6
SPC_SPECTRUM_DETAIL_COL = 7
SPC_SPECTRUM_INTERACTION_COL = 8
SPC_SPECTRUM_INTERACTION_SPACE_COL = 9
SPC_SPECTRUM_INTERACTION_DETAIL_COL = 10

def write_header_in_result_file(row, sheet):
    sheet.write(row, SPECTRUM_COL, "SPECTRUM")
    sheet.write(row, SPECTRUM_SPACE_COL, "SPECTRUM_SPACE")
    sheet.write(row, SPECTRUM_DETAIL_COL, "SPECTRUM_DETAIL")
    sheet.write(row, SPC_SPECTRUM_COL, "SPC_SPECTRUM")
    sheet.write(row, SPC_SPECTRUM_SPACE_COL, "SPC_SPECTRUM_SPACE")
    sheet.write(row, SPC_SPECTRUM_DETAIL_COL, "SPC_SPECTRUM_DETAIL")
    sheet.write(row, SPC_SPECTRUM_INTERACTION_COL, "SPC_SPECTRUM_INTERACTION")
    sheet.write(row, SPC_SPECTRUM_INTERACTION_SPACE_COL, "SPC_SPECTRUM_INTERACTION_SPACE")
    sheet.write(row, SPC_SPECTRUM_INTERACTION_DETAIL_COL, "SPC_SPECTRUM_INTERACTION_DETAIL")


def write_results_to_file(row, sheet, ranking_results):

    for item in ranking_results:

        sheet.write(row, VARIANT_COL, item)
        spectrum_rank = ranking_results[item][RankingManager.RANKING_SPECTRUM]
        sheet.write(row, SPECTRUM_COL, spectrum_rank)
        sheet.write(row, SPECTRUM_SPACE_COL, len(ranking_results[item][RankingManager.RANKING_SPECTRUM_DETAIL]))
        sheet.write(row, SPECTRUM_DETAIL_COL, str(ranking_results[item][RankingManager.RANKING_SPECTRUM_DETAIL][0:spectrum_rank]))

        spc_spectrum_rank = ranking_results[item][RankingManager.RANKING_SPC_SPECTRUM]
        sheet.write(row, SPC_SPECTRUM_COL,spc_spectrum_rank)
        sheet.write(row, SPC_SPECTRUM_SPACE_COL, len(ranking_results[item][RankingManager.RANKING_SPC_SPECTRUM_DETAIL]))
        sheet.write(row, SPC_SPECTRUM_DETAIL_COL,
                    str(ranking_results[item][RankingManager.RANKING_SPC_SPECTRUM_DETAIL][0:spc_spectrum_rank]))

        spc_spectrum_interaction_rank = ranking_results[item][RankingManager.RANKING_SPC_SPECTRUM_INTERACTION]
        sheet.write(row, SPC_SPECTRUM_INTERACTION_COL, spc_spectrum_interaction_rank)
        sheet.write(row, SPC_SPECTRUM_INTERACTION_SPACE_COL, len(ranking_results[item][
                                                                     RankingManager.RANKING_SPC_SPECTRUM_INTERACTION_DETAIL]))
        sheet.write(row, SPC_SPECTRUM_INTERACTION_DETAIL_COL,
                    str(ranking_results[item][RankingManager.RANKING_SPC_SPECTRUM_INTERACTION_DETAIL][0:spc_spectrum_interaction_rank]))
        row += 1
    return row

def ranking( project_name, filtering_coverage_rate):

    experiment_file_name = join_path(EXPERIMENT_RESULT_FOLDER, project_name + "_" + str(filtering_coverage_rate) + "_result.xlsx")
    wb = Workbook(experiment_file_name)
    project_dir = get_project_dir(project_name)

    sheet = wb.add_worksheet()
    row = 1
    write_header_in_result_file(row, sheet)
    row += 1
    mutated_projects_dir = get_mutated_projects_dir(project_dir)
    mutated_projects = list_dir(mutated_projects_dir)

    for mutated_project_name in mutated_projects:
        try:
            ranking_project = project_name + "_" + mutated_project_name

            logging.info("Ranking... %s", ranking_project)

            sheet.write(row, MUTATED_PROJECT_COL, mutated_project_name)

            mutated_project_dir = MutantManager.get_mutated_project_dir(project_dir, mutated_project_name)

            spc_log_file_path = SPCsManager.find_SPCs(mutated_project_dir, filtering_coverage_rate)

            SlicingManager.do_slice(spc_log_file_path)
            suspicious_stms_list = get_suspicious_statement(mutated_project_dir)
            buggy_statement = get_buggy_statement(mutated_project_name, mutated_project_dir)

            ranking_results = RankingManager.ranking(buggy_statement, mutated_project_dir,
                                                     suspicious_stms_list)
            row = write_results_to_file(row, sheet, ranking_results)
            row += 1
        except:
            logging.info(" Exception in ranking %s", mutated_project_name)
    wb.close()


if __name__ == "__main__":

    project_name = "ProjectTest2"

    #filtering_coverage_rate_list = [1, 0.95, 0.9, 0.8, 0.5]
    filtering_coverage_rate_list = [0.95]
    for i in range(0, len(filtering_coverage_rate_list)):
         ranking(project_name, filtering_coverage_rate_list[i])






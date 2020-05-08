import logging
import os
import time

from FileManager import get_project_dir, get_mutated_projects_dir, join_path, EXPERIMENT_RESULT_FOLDER
import MutantManager
import RankingManager
from SuspiciousStatementManager import get_suspicious_statement, get_buggy_statement
import threading
from xlsxwriter import Workbook

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

def thread_function( project_name):
    experiment_file_name = join_path(EXPERIMENT_RESULT_FOLDER, project_name + "_result.xlsx")
    wb = Workbook(experiment_file_name)
    project_dir = get_project_dir(project_name)
    sheet = wb.add_worksheet()
    row = 1
    write_header_in_result_file(row, sheet)
    row += 1
    mutated_projects_dir = get_mutated_projects_dir(project_dir)
    mutated_projects = os.listdir(mutated_projects_dir)

    for mutated_project_name in mutated_projects:
        mutated_project_dir = MutantManager.get_mutated_project_dir(project_dir, mutated_project_name)
        suspicious_stms_list = get_suspicious_statement(mutated_project_dir)
        sheet.write(row, MUTATED_PROJECT_COL, mutated_project_name)
        buggy_statement = get_buggy_statement(mutated_project_name, mutated_project_dir)
        ranking_results = RankingManager.ranking(buggy_statement, mutated_project_dir,
                                                 suspicious_stms_list)
        write_results_to_file(row, sheet, ranking_results)
        row += 1

    wb.close()

if __name__ == "__main__":

    project_names = ["ProjectTest1", "ProjectTest2"]


    logging.info("Main    : before creating thread")
    x = threading.Thread(target=thread_function, args=(project_names[0],))
    y = threading.Thread(target=thread_function, args=(project_names[1],))

    logging.info("Main    : before running thread")
    x.start()
    y.start()
    logging.info("Main    : wait for the thread to finish")
    # x.join()

    logging.info("Main    : all done")













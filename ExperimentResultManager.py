import logging
import threading
import time

import SPCsManager
import SlicingManager
from FileManager import get_project_dir, get_mutated_projects_dir, join_path, EXPERIMENT_RESULT_FOLDER, list_dir, \
    get_spc_log_file_path, RUNTIME_LOG_FOLDER
import MutantManager
import RankingManager
from SuspiciousStatementManager import get_suspicious_statement, get_buggy_statement
from xlsxwriter import Workbook
import pandas as pd


MUTATED_PROJECT_COL = 0
VARIANT_COL = 1
SPECTRUM_COL = 2
SPECTRUM_SPACE_COL = 3
SPECTRUM_DETAIL_COL = 4
SPECTRUM_TIME_COL = 5
SPC_SPECTRUM_COL = 6
SPC_SPECTRUM_SPACE_COL = 7
SPC_SPECTRUM_DETAIL_COL = 8
SPC_SPECTRUM_TIME_COL = 9
SPC_SPECTRUM_INTERACTION_COL = 10
SPC_SPECTRUM_INTERACTION_SPACE_COL = 11
SPC_SPECTRUM_INTERACTION_DETAIL_COL = 12
SPC_SPECTRUM_INTERACTION_TIME_COL = 13


MUTATED_PROJECT_HEADER = "MUTATED_PROJECT"
VARIANT_HEADER = "VARIANT"
SPECTRUM_HEADER = "SPECTRUM"
SPECTRUM_SPACE_HEADER = "SPECTRUM_SPACE"
SPECTRUM_DETAIL_HEADER = "SPECTRUM_DETAIL"
SPECTRUM_TIME_HEADER = "SPECTRUM_RANKING_TIME"
SPC_SPECTRUM_HEADER = "SPC_SPECTRUM"
SPC_SPECTRUM_SPACE_HEADER = "SPC_SPECTRUM_SPACE"
SPC_SPECTRUM_DETAIL_HEADER = "SPC_SPECTRUM_DETAIL"
SPC_SPECTRUM_TIME_HEADER = "SPC_SPECTRUM_RANKING_TIME"
SPC_SPECTRUM_INTERACTION_HEADER = "SPC_SPECTRUM_INTERACTION"
SPC_SPECTRUM_INTERACTION_SPACE_HEADER = "SPC_SPECTRUM_INTERACTION_SPACE"
SPC_SPECTRUM_INTERACTION_DETAIL_HEADER = "SPC_SPECTRUM_INTERACTION_DETAIL"
SPC_SPECTRUM_INTERACTION_TIME_HEADER = "SPC_SPECTRUM_INTERACTION_RANKING_TIME"



THREAD_MUTATED_PROJECT = "MUTATED_PROJECT"
THREAD_FUNCTION = "FUNCTION"
THREAD_START_TIME = "START_TIME"
THREAD_RUN_TIME = "RUN_TIME"

LOG_SPC_DETECTION_RUNTIME = "LOG_SPC_DETECTION_RUNTIME"
LOG_SLICING_RUNTIME = "LOG_SLICING_RUNTIME"

def write_header_in_result_file(row, sheet):
    sheet.write(row, MUTATED_PROJECT_COL, MUTATED_PROJECT_HEADER)
    sheet.write(row, VARIANT_COL, VARIANT_HEADER)
    sheet.write(row, SPECTRUM_COL, SPECTRUM_HEADER)
    sheet.write(row, SPECTRUM_SPACE_COL, SPECTRUM_SPACE_HEADER)
    sheet.write(row, SPECTRUM_DETAIL_COL, SPECTRUM_DETAIL_HEADER)
    sheet.write(row, SPECTRUM_TIME_COL, SPECTRUM_TIME_HEADER)
    sheet.write(row, SPC_SPECTRUM_COL, SPC_SPECTRUM_HEADER)
    sheet.write(row, SPC_SPECTRUM_SPACE_COL, SPC_SPECTRUM_SPACE_HEADER)
    sheet.write(row, SPC_SPECTRUM_DETAIL_COL, SPC_SPECTRUM_DETAIL_HEADER)
    sheet.write(row, SPC_SPECTRUM_TIME_COL, SPC_SPECTRUM_TIME_HEADER)
    sheet.write(row, SPC_SPECTRUM_INTERACTION_COL, SPC_SPECTRUM_INTERACTION_HEADER)
    sheet.write(row, SPC_SPECTRUM_INTERACTION_SPACE_COL, SPC_SPECTRUM_INTERACTION_SPACE_HEADER)
    sheet.write(row, SPC_SPECTRUM_INTERACTION_DETAIL_COL, SPC_SPECTRUM_INTERACTION_DETAIL_HEADER)
    sheet.write(row, SPC_SPECTRUM_INTERACTION_TIME_COL, SPC_SPECTRUM_INTERACTION_TIME_HEADER)

def write_results_to_file(row, sheet, ranking_results):


    for item in ranking_results:

        sheet.write(row, VARIANT_COL, item)

        spectrum_rank = ranking_results[item][RankingManager.RANKING_SPECTRUM]
        sheet.write(row, SPECTRUM_COL, spectrum_rank)

        sheet.write(row, SPECTRUM_SPACE_COL, len(ranking_results[item][RankingManager.RANKING_SPECTRUM_DETAIL]))
        sheet.write(row, SPECTRUM_DETAIL_COL, str(ranking_results[item][RankingManager.RANKING_SPECTRUM_DETAIL][0:spectrum_rank]))
        sheet.write(row, SPECTRUM_TIME_COL,
                    str(ranking_results[item][RankingManager.RANKING_SPECTRUM_TIME]))

        spc_spectrum_rank = ranking_results[item][RankingManager.RANKING_SPC_SPECTRUM]
        sheet.write(row, SPC_SPECTRUM_COL,spc_spectrum_rank)
        sheet.write(row, SPC_SPECTRUM_SPACE_COL, len(ranking_results[item][RankingManager.RANKING_SPC_SPECTRUM_DETAIL]))
        sheet.write(row, SPC_SPECTRUM_DETAIL_COL,
                    str(ranking_results[item][RankingManager.RANKING_SPC_SPECTRUM_DETAIL][0:spc_spectrum_rank]))
        sheet.write(row, SPC_SPECTRUM_TIME_COL,
                    str(ranking_results[item][RankingManager.RANKING_SPC_SPECTRUM_TIME]))


        spc_spectrum_interaction_rank = ranking_results[item][RankingManager.RANKING_SPC_SPECTRUM_INTERACTION]
        sheet.write(row, SPC_SPECTRUM_INTERACTION_COL, spc_spectrum_interaction_rank)
        sheet.write(row, SPC_SPECTRUM_INTERACTION_SPACE_COL, len(ranking_results[item][
                                                                     RankingManager.RANKING_SPC_SPECTRUM_INTERACTION_DETAIL]))
        sheet.write(row, SPC_SPECTRUM_INTERACTION_DETAIL_COL,
                    str(ranking_results[item][RankingManager.RANKING_SPC_SPECTRUM_INTERACTION_DETAIL][0:spc_spectrum_interaction_rank]))
        sheet.write(row, SPC_SPECTRUM_INTERACTION_TIME_COL,
                    str(ranking_results[item][RankingManager.RANKING_SPC_SPECTRUM_INTERACTION_TIME]))

        row += 1

    return row

def log_run_time(log_file_name, threads, kind_of_log):
    log_file_path = join_path(RUNTIME_LOG_FOLDER, log_file_name + ".txt")
    file = open(log_file_path, "a")
    file.write(kind_of_log + "\n")
    for t in threads:
        file.write(t[THREAD_MUTATED_PROJECT]+ ": " + str(t[THREAD_RUN_TIME]) + "\n")
    file.close()

def detect_spcs(project_name, filtering_coverage_rate, experiment_file_name):
    project_dir = get_project_dir(project_name)
    mutated_projects_dir = get_mutated_projects_dir(project_dir)
    mutated_projects = list_dir(mutated_projects_dir)

    threads = []
    for i in range(0, len(mutated_projects)):
        current_thread = {}
        current_project = project_name + "_" + mutated_projects[i]
        current_thread[THREAD_MUTATED_PROJECT] = current_project
        logging.info("Find SPC in ... %s", current_project)

        mutated_project_dir = MutantManager.get_mutated_project_dir(project_dir, mutated_projects[i])

        current_thread[THREAD_FUNCTION] = threading.Thread(target=SPCsManager.find_SPCs,
                                                           args=(mutated_project_dir, filtering_coverage_rate))
        current_thread[THREAD_FUNCTION].start()
        current_thread[THREAD_START_TIME] = time.time()
        threads.append(current_thread)

    for i in range(0, len(mutated_projects)):
        threads[i][THREAD_FUNCTION].join()
        threads[i][THREAD_RUN_TIME] = time.time() - threads[i][THREAD_START_TIME]

    log_run_time(experiment_file_name, threads, LOG_SPC_DETECTION_RUNTIME)


def slicing(project_name, experiment_file_name):
    project_dir = get_project_dir(project_name)
    mutated_projects_dir = get_mutated_projects_dir(project_dir)
    mutated_projects = list_dir(mutated_projects_dir)

    threads = []
    for i in range(0, len(mutated_projects)):
        current_thread = {}
        current_project = project_name + "_" + mutated_projects[i]
        current_thread[THREAD_MUTATED_PROJECT] = current_project
        logging.info("slicing ... %s", current_project)

        mutated_project_dir = MutantManager.get_mutated_project_dir(project_dir, mutated_projects[i])
        spc_log_file_path = get_spc_log_file_path(mutated_project_dir)

        current_thread[THREAD_FUNCTION] = threading.Thread(target=SlicingManager.do_slice,
                                                           args=(str(spc_log_file_path),))
        current_thread[THREAD_FUNCTION].start()
        current_thread[THREAD_START_TIME] = time.time()
        threads.append(current_thread)

    for i in range(0, len(mutated_projects)):
        threads[i][THREAD_FUNCTION].join()
        threads[i][THREAD_RUN_TIME] = time.time() - threads[i][THREAD_START_TIME]

    log_run_time(experiment_file_name, threads, LOG_SLICING_RUNTIME)


def ranking_with_coverage_rate( project_name, filtering_coverage_rate, ranking_types):
    sheet = []
    project_dir = get_project_dir(project_name)
    row = 0

    experiment_file_name =  project_name + "_coverage" + str(filtering_coverage_rate) + "_"+ str(time.time())
    experiment_file_path = join_path(EXPERIMENT_RESULT_FOLDER, experiment_file_name+  ".xlsx")
    wb= Workbook(experiment_file_path)

    for i in range(0, len(ranking_types)):
        sheet.append(wb.add_worksheet(ranking_types[i]))
        write_header_in_result_file(row, sheet[i])

    row += 1
    mutated_projects_dir = get_mutated_projects_dir(project_dir)
    mutated_projects = list_dir(mutated_projects_dir)

    detect_spcs(project_name, filtering_coverage_rate, experiment_file_name)
    slicing(project_name, experiment_file_name)
    for mutated_project_name in mutated_projects:
        try:
            ranking_project = project_name + "_" + mutated_project_name

            logging.info("Ranking... %s", ranking_project)
            mutated_project_dir = MutantManager.get_mutated_project_dir(project_dir, mutated_project_name)

            suspicious_stms_list = get_suspicious_statement(mutated_project_dir)
            buggy_statement = get_buggy_statement(mutated_project_name, mutated_project_dir)

            row_temp = row
            for i in range(0, len(ranking_types)):
                ranking_results = RankingManager.ranking(buggy_statement, mutated_project_dir,
                                                     suspicious_stms_list, ranking_types[i])

                sheet[i].write(row_temp, MUTATED_PROJECT_COL, mutated_project_name)
                row = write_results_to_file(row_temp, sheet[i], ranking_results)

        except:
            logging.info(" Exception in ranking %s", mutated_project_name)

    wb.close()


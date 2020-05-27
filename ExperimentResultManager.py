import logging
import time

import SPCsManager
import SlicingManager
from FileManager import get_project_dir, get_mutated_projects_dir, join_path, EXPERIMENT_RESULT_FOLDER, list_dir
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
RUM_TIME_COL = 14

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

RUM_TIME_HEADER = "RUN_TIME"

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
    sheet.write(row, RUM_TIME_COL, RUM_TIME_HEADER)

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

def ranking_with_coverate_rate( project_name, filtering_coverage_rate, ranking_types):


    sheet = []
    project_dir = get_project_dir(project_name)
    row = 0

    experiment_file_name = join_path(EXPERIMENT_RESULT_FOLDER, project_name + "_coverage" + str(filtering_coverage_rate) + "_"+ str(time.time()) + ".xlsx")
    wb= Workbook(experiment_file_name)

    for i in range(0, len(ranking_types)):
        sheet.append(wb.add_worksheet(ranking_types[i]))
        write_header_in_result_file(row, sheet[i])

    row += 1
    mutated_projects_dir = get_mutated_projects_dir(project_dir)
    mutated_projects = list_dir(mutated_projects_dir)

    for mutated_project_name in mutated_projects:
        try:
            start_time = time.time()
            ranking_project = project_name + "_" + mutated_project_name

            logging.info("Ranking... %s", ranking_project)


            mutated_project_dir = MutantManager.get_mutated_project_dir(project_dir, mutated_project_name)

            spc_log_file_path = SPCsManager.find_SPCs(mutated_project_dir, filtering_coverage_rate)

            SlicingManager.do_slice(spc_log_file_path)
            suspicious_stms_list = get_suspicious_statement(mutated_project_dir)
            buggy_statement = get_buggy_statement(mutated_project_name, mutated_project_dir)

            row_temp = row
            for i in range(0, len(ranking_types)):
                ranking_results = RankingManager.ranking(buggy_statement, mutated_project_dir,
                                                     suspicious_stms_list, ranking_types[i])

                sheet[i].write(row_temp, MUTATED_PROJECT_COL, mutated_project_name)
                row = write_results_to_file(row_temp, sheet[i], ranking_results)
                sheet[i].write(row-1, RUM_TIME_COL, (time.time() - start_time))
            row += 1

        except:
            logging.info(" Exception in ranking %s", mutated_project_name)

    wb.close()

def num_of_bugs(df):
    bugs = 0
    for i in range(0, len(df[SPECTRUM_HEADER])):
        if (not pd.isna(df[SPECTRUM_HEADER][i]) and not pd.isna(df[MUTATED_PROJECT_HEADER][i])):
            bugs += 1
    return bugs

def summary_experiment_result(file_name):
    df = pd.read_excel(file_name)

    spectrum_sum = 0
    spectrum_quantity = 0
    spectrum_space_sum = 0
    for i in range(0,len(df[SPECTRUM_HEADER])):
        if(not pd.isna(df[SPECTRUM_HEADER][i])):

            spectrum_sum += df[SPECTRUM_HEADER][i]
            spectrum_space_sum += df[SPECTRUM_SPACE_HEADER][i]
            spectrum_quantity += 1

    if(spectrum_quantity != 0):
        print("spectrum_avg", spectrum_sum/spectrum_quantity)
        print("spectrum_space_avg", spectrum_space_sum / spectrum_quantity)
    else:
        print("spectrum_avg", 0)
        print("spectrum_space_avg", 0)

    spc_spectrum_sum = 0
    spc_spectrum_quantity = 0
    spc_spectrum_space_sum = 0
    for i in range(0, len(df[SPC_SPECTRUM_HEADER])):
        if (not pd.isna(df[SPC_SPECTRUM_HEADER][i])):
            spc_spectrum_sum += df[SPC_SPECTRUM_HEADER][i]
            spc_spectrum_space_sum += df[SPC_SPECTRUM_SPACE_HEADER][i]
            spc_spectrum_quantity += 1

    if (spc_spectrum_quantity != 0):
        print("spc_spectrum_avg", spc_spectrum_sum / spc_spectrum_quantity)
        print("spc_spectrum_space_avg", spc_spectrum_space_sum / spc_spectrum_quantity)
    else:
        print("spc_spectrum_avg", 0)
        print("spc_spectrum_space_avg", 0)

    spc_spectrum_interaction_sum = 0
    spc_spectrum_interaction_quantity = 0
    spc_spectrum_interaction_space_sum = 0
    for i in range(0, len(df[SPC_SPECTRUM_INTERACTION_HEADER])):
        if (not pd.isna(df[SPC_SPECTRUM_INTERACTION_HEADER][i])):
            spc_spectrum_interaction_sum += df[SPC_SPECTRUM_INTERACTION_HEADER][i]
            spc_spectrum_interaction_space_sum += df[SPC_SPECTRUM_INTERACTION_SPACE_HEADER][i]
            spc_spectrum_interaction_quantity += 1

    if (spc_spectrum_interaction_quantity != 0):
        print("spc_spectrum_interaction_avg", spc_spectrum_interaction_sum / spc_spectrum_interaction_quantity)
        print("spc_spectrum_interaction_space_avg", spc_spectrum_interaction_space_sum / spc_spectrum_interaction_quantity)
    else:
        print("spc_spectrum_interaction_avg", 0)
        print("spc_spectrum_interaction_space_avg", 0)

    print("num_of_bugs", num_of_bugs(df))

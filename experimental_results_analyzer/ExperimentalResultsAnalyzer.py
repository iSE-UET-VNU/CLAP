import os


import pandas

from FileManager import join_path, EXPERIMENT_RESULT_FOLDER
from ranking.Keywords import SBFL_METRIC, VARCOP_VS_SBFL_IN_RANK, VARCOP_VS_SBFL_IN_EXAM, \
    VARCOP_DISABLE_BPC_VS_SBFL_IN_RANK, VARCOP_DISABLE_BPC_VS_SBFL_IN_EXAM, VARCOP_EXAM, VARCOP_DISABLE_BPC_EXAM, \
    SBFL_EXAM, FB_RANK, FB_EXAM, BUG_ID, BUGGY_STM, NUM_CASES, NUM_BUGS
from ranking.RankingManager import VARCOP_RANK, VARCOP_SPACE, VARCOP_DISABLE_BPC_RANK, SBFL_RANK, SPACE
from ranking.Spectrum_Expression import JACCARD, SORENSEN_DICE, TARANTULA, OCHIAI, OP2, BARINEL, DSTAR, ROGERS_TANIMOTO, \
    AMPLE, \
    SIMPLE_MATCHING, RUSSELL_RAO, COHEN, SCOTT, ROGOT1, GEOMETRIC_MEAN, M2, WONG1, SOKAL, DICE, HUMANN, OVERLAP, ZOLTAR, \
    WONG3, WONG2, M1, ROGOT2, EUCLID, HAMMING, FLEISS, ANDERBERG, KULCZYNSKI1, KULCZYNSKI2, HARMONIC_MEAN, GOODMAN

from xlsxwriter import Workbook

data_column = [VARCOP_RANK, VARCOP_EXAM, VARCOP_SPACE, VARCOP_DISABLE_BPC_RANK, VARCOP_DISABLE_BPC_EXAM, SBFL_RANK, SBFL_EXAM, FB_RANK, FB_EXAM, SPACE]
SBFL_METRIC_COL = 0
NUM_CASES_COL = 1
NUM_BUGS_COL = 2
VARCOP_RANK_COL = 3
VARCOP_EXAM_COL = 4
VARCOP_SPACE_COL = 5
VARCOP_DISABLE_BPC_RANK_COL = 6
VARCOP_DISABLE_BPC_EXAM_COL = 7
SBFL_RANK_COL = 8
SBFL_EXAM_COL = 9
FB_RANK_COL = 10
FB_EXAM_COL = 11
SPACE_COL = 12

# comparion
ISOLATION_VS_SBFL_IN_RANK_COL = 13
ISOLATION_VS_SBFL_IN_EXAM_COL = 14
WITHOUT_ISOLATION_VS_SBFL_IN_RANK_COL = 15
WITHOUT_ISOLATION_VS_SBFL_IN_EXAM_COL = 16

SPECTRUM_EXPRESSIONS_LIST = [TARANTULA, OCHIAI, OP2, BARINEL, DSTAR,
                             RUSSELL_RAO, SIMPLE_MATCHING, ROGERS_TANIMOTO, AMPLE, JACCARD,
                             COHEN, SCOTT, ROGOT1, GEOMETRIC_MEAN, M2,
                             WONG1, SOKAL, SORENSEN_DICE, DICE, HUMANN, WONG2, ZOLTAR,
                             EUCLID, ROGOT2, HAMMING, FLEISS, ANDERBERG,
                             GOODMAN, HARMONIC_MEAN, KULCZYNSKI2]


# SPECTRUM_EXPRESSIONS_LIST = [TARANTULA]

def write_all_bugs_to_a_file(summary_file_dir, file_lists, num_of_bugs, base_path):

    writer = pandas.ExcelWriter(summary_file_dir, engine='openpyxl')

    row = 0
    num_of_file = 0
    for file in file_lists:
        for b in num_of_bugs:
            file_name = join_path(file, b + ".xlsx")
            file_path = join_path(base_path, file_name)
            if os.path.exists(file_path):
                excel_data_df = pandas.read_excel(file_path, sheet_name=None)
                num_of_file += 1
                if num_of_file > 1:
                    for spectrum_expression_type in SPECTRUM_EXPRESSIONS_LIST:
                        excel_data_df[spectrum_expression_type].to_excel(writer, sheet_name=spectrum_expression_type, startrow=row,
                                                                         index=False, header=False)
                    row += len(excel_data_df[TARANTULA])
                else:
                    for spectrum_expression_type in SPECTRUM_EXPRESSIONS_LIST:
                        excel_data_df[spectrum_expression_type].to_excel(writer, sheet_name=spectrum_expression_type, startrow=row,
                                                                         index=False)
                    row += len(excel_data_df[TARANTULA]) + 1

    writer.save()


def summary_hitx(hitx_file_dir, all_bugs_file_dir):
    wb = Workbook(hitx_file_dir)
    sheet = wb.add_worksheet("sheet1")

    row = 0
    sheet.write(row, 1, "HIT@1")
    sheet.write(row, 3, "HIT@2")
    sheet.write(row, 5, "HIT@3")
    sheet.write(row, 7, "HIT@4")
    sheet.write(row, 9, "HIT@5")
    row += 1
    sheet.write(row, 0, "Metric")
    sheet.write(row, 1, "VarCop")
    sheet.write(row, 2, "SBFL")
    sheet.write(row, 3, "VarCop")
    sheet.write(row, 4, "SBFL")
    sheet.write(row, 5, "VarCop")
    sheet.write(row, 6, "SBFL")
    sheet.write(row, 7, "VarCop")
    sheet.write(row, 8, "SBFL")
    sheet.write(row, 9, "VarCop")
    sheet.write(row, 10, "SBFL")
    row += 1

    excel_data_df = pandas.read_excel(all_bugs_file_dir, sheet_name=None)

    for spectrum_expression_type in SPECTRUM_EXPRESSIONS_LIST:
        sheet.write(row, 0, spectrum_expression_type)
        hit_list = [1, 2, 3, 4, 5]
        col = 0;
        for index in range(0, len(hit_list)):
            col += 1
            sheet.write(row, col, count_hit_x(excel_data_df[spectrum_expression_type][VARCOP_RANK], hit_list[index]))
            col += 1
            sheet.write(row, col,
                        count_hit_x(excel_data_df[spectrum_expression_type][SBFL_RANK],
                                    hit_list[index]))
        row += 1

    wb.close()


def count_hit_x(value_list, x):
    count = 0
    for value in value_list:
        if type(value) != str and value != -1 and value <= x:
            count += 1
    return count


def summary_result(all_bugs_file, summary_file):
    summary_file_dir = join_path(EXPERIMENT_RESULT_FOLDER,
                                 summary_file)
    wb = Workbook(summary_file_dir)
    sheet = wb.add_worksheet("sheet1")

    row = 0
    write_header_in_sumary_file(row, sheet)
    row += 1
    row = calculate_average_in_a_file(all_bugs_file, row, sheet)

    wb.close()


def write_header_in_sumary_file(row, sheet):
    sheet.write(row, SBFL_METRIC_COL, SBFL_METRIC)
    sheet.write(row, NUM_CASES_COL, NUM_CASES)
    sheet.write(row, NUM_BUGS_COL, NUM_BUGS)
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
    write_header_for_comparion(row, sheet)


def write_header_for_comparion(row, sheet):
    sheet.write(row, ISOLATION_VS_SBFL_IN_RANK_COL, VARCOP_VS_SBFL_IN_RANK)
    sheet.write(row, ISOLATION_VS_SBFL_IN_EXAM_COL, VARCOP_VS_SBFL_IN_EXAM)
    sheet.write(row, WITHOUT_ISOLATION_VS_SBFL_IN_RANK_COL, VARCOP_DISABLE_BPC_VS_SBFL_IN_RANK)
    sheet.write(row, WITHOUT_ISOLATION_VS_SBFL_IN_EXAM_COL, VARCOP_DISABLE_BPC_VS_SBFL_IN_EXAM)


def num_of_element(data_list):
    element_count = 0
    for r in data_list:
        if not pandas.isnull(r):
            element_count += 1
    return element_count


def calculate_average_in_a_file(experimental_file_dir, row, sheet):
    excel_data_df = pandas.read_excel(experimental_file_dir, sheet_name=None)

    for spectrum_expression_type in SPECTRUM_EXPRESSIONS_LIST:
        num_of_cases = num_of_element(excel_data_df[spectrum_expression_type][BUG_ID])
        sheet.write(row, NUM_CASES_COL, num_of_cases)

        num_of_bugs = num_of_element(excel_data_df[spectrum_expression_type][BUGGY_STM])
        sheet.write(row, NUM_BUGS_COL, num_of_bugs)

        sheet.write(row, SBFL_METRIC_COL, spectrum_expression_type)

        average_value_list = average_best_rank_exam(excel_data_df, spectrum_expression_type)
        col = VARCOP_RANK_COL
        for metric in data_column:
            sheet.write(row, col, average_value_list[metric])
            col += 1

        row += 1

    return row



def count_total_bugs(files_list):
    bug_list = []
    overall_info = {}

    for file in files_list.keys():
        excel_data = pandas.read_excel(files_list[file], sheet_name=None)
        overall_info[file] = excel_data

    for file in overall_info.keys():
        for bug in overall_info[file][TARANTULA][BUG_ID]:
            if bug not in bug_list:
                print(bug)
                bug_list.append(bug)
    return len(bug_list)

MAX = 100000
MIN = -100000



def percentage_of_bugs_found(multiple_bugs_file, sbfl_metric, examined_statements):
    excel_data_df = pandas.read_excel(multiple_bugs_file, sheet_name=None)
    results = {}
    for num in examined_statements:
        sum_varcop = 0
        sum_sbfl = 0
        num_of_cases = 0
        count = 0
        for i in range(0, len(excel_data_df[sbfl_metric][BUG_ID])):
            if (excel_data_df[sbfl_metric][BUG_ID][i] != BUG_ID and not pandas.isnull(
                    excel_data_df[sbfl_metric][BUG_ID][i])):
                if (count != 0):
                    sum_varcop += varcop / count
                    sum_sbfl += sbpl / count
                    num_of_cases += 1
                varcop = 0
                sbpl = 0
                count = 0

            varcop_rank = excel_data_df[sbfl_metric]["VARCOP:RANK"][i]
            sbfl_rank = excel_data_df[sbfl_metric]["SBFL:RANK"][i]

            if (type(varcop_rank) == int and varcop_rank != -1 and varcop_rank <= num):
                varcop += 1
            if (type(sbfl_rank) == int and sbfl_rank != -1 and sbfl_rank <= num):
                sbpl += 1
            count += 1
        results[num] = {}
        results[num]["varcop"] = sum_varcop / num_of_cases
        results[num]["sbfl"] = sum_sbfl / num_of_cases
    return results


def calculate_average(data):
    sum = 0
    for item in data:
        sum += item
    return sum/len(data)

def average_best_rank_exam(excel_data_df, sbfl_metric):
    best_value_list = get_best_rank_exam(excel_data_df, sbfl_metric)
    average_value_list = {}
    for metric in data_column:
        average_value_list[metric] = calculate_average(best_value_list[metric])
    return average_value_list

def average_worst_rank_exam(excel_data_df, sbfl_metric):
    best_value_list = get_worst_rank_exam(excel_data_df, sbfl_metric)
    average_value_list = {}
    for metric in data_column:
        average_value_list[metric] = calculate_average(best_value_list[metric])
    return average_value_list

def get_best_rank_exam(excel_data_df, sbfl_metric):
    index = 0
    best_value_list = {}
    for metric in data_column:
        best_value_list[metric] = []

    while index < len(excel_data_df[sbfl_metric][BUG_ID]):
        data, index = get_values_of_a_case(excel_data_df, sbfl_metric, index)
        for metric in data_column:
            best_value_list[metric].append(min(data[metric]))
    return best_value_list

def get_worst_rank_exam(excel_data_df, sbfl_metric):
    index = 0
    best_value_list = {}
    for metric in data_column:
        best_value_list[metric] = []

    while index < len(excel_data_df[sbfl_metric][BUG_ID]):
        data, index = get_values_of_a_case(excel_data_df, sbfl_metric, index)
        for metric in data_column:
            best_value_list[metric].append(max(data[metric]))
    return best_value_list

def get_values_of_a_case(excel_data_df, sbfl_metric, index):
    data = {}
    for metric in data_column:
        data[metric] = []
        data[metric].append(excel_data_df[sbfl_metric][metric][index])
    index += 1
    while index < len(excel_data_df[sbfl_metric][BUG_ID]) and pandas.isnull(excel_data_df[sbfl_metric][BUG_ID][index]):
        for metric in data_column:
            data[metric].append(excel_data_df[sbfl_metric][metric][index])
        index += 1
    return data, index


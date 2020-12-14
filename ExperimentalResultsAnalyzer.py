import os
import pandas

from ExperimentResultManager import VARCOP_SPC_FAILING_HEADER, VARCOP_SPC_LAYER_HEADER, VARCOP_SPC_SPACE_HEADER, \
    SPECTRUM_HEADER, SPECTRUM_SPACE_HEADER, FEATURE_HEADER, FEATURE_STM_HEADER, FEATURE_SPACE_HEADER, \
    MUTATED_PROJECT_HEADER, VARCOP_FAILING_HEADER, VARCOP_LAYER_HEADER, VARCOP_SPACE_HEADER
from FileManager import join_path, EXPERIMENT_RESULT_FOLDER
from Spectrum_Expression import RUSSELL_RAO, SIMPLE_MATCHING, ROGERS_TANIMOTO, AMPLE, JACCARD, COHEN, SCOTT, ROGOT1, \
    GEOMETRIC_MEAN, M2, TARANTULA, OCHIAI, OP2, BARINEL, DSTAR, WONG1, SOKAL, KULCZYNSKI2, GOODMAN, HARMONIC_MEAN, \
    EUCLID, KULCZYNSKI1, WONG2, M1, WONG3, ROGOT2, HAMMING, FLEISS, ANDERBERG, ZOLTAR, OVERLAP, SORENSEN_DICE, DICE, \
    HUMANN
from xlsxwriter import Workbook

SYSTEM_COL_HEADER = "SYSTEM"
K_WISE_HEADER = "K_WISE"
EXPERIMENTAL_FILE_HEADER = "EXPERIMENTAL_RESULT_FILE"
SPECTRUM_EXPRESSION_HEADER = "SPECTRUM_EXPRESSION"
NUM_DETECTED_BUGS_HEADER = "NUM_OF_DETECTED_BUGS"
SPC_FAILING_ONLY_EXAM_HEADER = "SPC_FAILING_ONLY_EXAM"
SPC_LAYER_EXAM_HEADER = "SPC_LAYER_EXAM"
WITHOUT_ISOLATION_F_EXAM_HEADER = "WITHOUT_ISOLATION_F_EXAM_HEADER"
WITHOUT_ISOLATION_LAYER_EXAM_HEADER = "WITHOUT_ISOLATION_LAYER_EXAM_HEADER"
SPECTRUM_EXAM_HEADER = "SPECTRUM_EXAM"
FEATURE_STM_EXAM_HEADER = "FEATURE_STM_EXAM"

SYSTEM_COL = 0
K_WISE_COL = 1
EXPERIMENTAL_FILE_COL = 2
SPECTRUM_EXPRESSION_COL = 3
NUM_DETECTED_BUGS_COL = 4
SPC_FAILING_ONLY_COL = 5
SPC_FAILING_ONLY_EXAM_COL = 6
SPC_LAYER_COL = 7
SPC_LAYER_EXAM_COL = 8
SPC_SPACE_COL = 9
WITHOUT_ISOLATION_F_COL = 10
WITHOUT_ISOLATION_F_EXAM_COL = 11
WITHOUT_ISOLATION_LAYER_COL  = 12
WITHOUT_ISOLATION_LAYER_EXAM_COL = 13
WITHOUT_ISOLATION_SPACE_COL = 14
SPECTRUM_COL = 15
SPECTRUM_EXAM_COL = 16
SPECTRUM_SPACE_COL = 17
FEATURE_COL = 18
FEATURE_STM_COL = 19
FEATURE_STM_EXAM_COL = 20
FEATURE_SPACE_COL = 21

SPECTRUM_EXPRESSIONS_LIST = [TARANTULA, OCHIAI, OP2, BARINEL, DSTAR,
                                                RUSSELL_RAO, SIMPLE_MATCHING, ROGERS_TANIMOTO, AMPLE, JACCARD,
                                                COHEN, SCOTT, ROGOT1, GEOMETRIC_MEAN, M2,
                                                WONG1, SOKAL, SORENSEN_DICE, DICE, HUMANN,
                                                 WONG2, WONG3, ZOLTAR, ROGOT2, HAMMING, FLEISS, ANDERBERG,
                                                GOODMAN, HARMONIC_MEAN, KULCZYNSKI2]
def write_all_bugs_to_a_file(summary_file_dir, file_lists):
    writer = pandas.ExcelWriter(summary_file_dir, engine='openpyxl')

    row = 0
    for file in file_lists:

        excel_data_df = pandas.read_excel(file, sheet_name=None)
        for spectrum_expression_type in SPECTRUM_EXPRESSIONS_LIST:
            excel_data_df[spectrum_expression_type].to_excel(writer, sheet_name=spectrum_expression_type, startrow=row,
                                                             index=False)
        row += len(excel_data_df[WONG3]) + 1
    writer.save()


def summary_hitx(hitx_file_dir, all_bugs_file_dir):

    wb = Workbook(hitx_file_dir)
    sheet = wb.add_worksheet("sheet1")

    row = 0
    sheet.write(row, 2, "HIT@1")
    sheet.write(row, 4, "HIT@2")
    sheet.write(row, 6, "HIT@3")
    sheet.write(row, 8, "HIT@4")
    sheet.write(row, 10, "HIT@5")
    row += 1
    sheet.write(row, 0, "File")
    sheet.write(row, 1, "Technique")
    sheet.write(row, 2, "VarCop")
    sheet.write(row, 3, "Spectrum")
    sheet.write(row, 4, "VarCop")
    sheet.write(row, 5, "Spectrum")
    sheet.write(row, 6, "VarCop")
    sheet.write(row, 7, "Spectrum")
    sheet.write(row, 8, "VarCop")
    sheet.write(row, 9, "Spectrum")
    sheet.write(row, 10, "VarCop")
    sheet.write(row, 11, "Spectrum")
    row += 1


    excel_data_df = pandas.read_excel(all_bugs_file_dir, sheet_name=None)

    for spectrum_expression_type in SPECTRUM_EXPRESSIONS_LIST:
        sheet.write(row, 1, spectrum_expression_type)
        hit_list = [1, 2, 3, 4, 5]
        col = 1;
        for index in range(0, len(hit_list)):
            col += 1
            sheet.write(row, col, count_hit_x(excel_data_df[spectrum_expression_type][VARCOP_SPC_LAYER_HEADER], hit_list[index]))
            col += 1
            sheet.write(row, col,
                        count_hit_x(excel_data_df[spectrum_expression_type][SPECTRUM_HEADER],
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
    sheet.write(row, SYSTEM_COL, SYSTEM_COL_HEADER)
    sheet.write(row, K_WISE_COL, K_WISE_HEADER)
    sheet.write(row, EXPERIMENTAL_FILE_COL, EXPERIMENTAL_FILE_HEADER)
    sheet.write(row, SPECTRUM_EXPRESSION_COL, SPECTRUM_EXPRESSION_HEADER)
    sheet.write(row, NUM_DETECTED_BUGS_COL, NUM_DETECTED_BUGS_HEADER)
    sheet.write(row, SPC_FAILING_ONLY_COL, VARCOP_SPC_FAILING_HEADER)
    sheet.write(row, SPC_FAILING_ONLY_EXAM_COL, SPC_FAILING_ONLY_EXAM_HEADER)
    sheet.write(row, SPC_LAYER_COL, VARCOP_SPC_LAYER_HEADER)
    sheet.write(row, SPC_LAYER_EXAM_COL, SPC_LAYER_EXAM_HEADER)
    sheet.write(row, SPC_SPACE_COL, VARCOP_SPC_SPACE_HEADER)
    sheet.write(row, WITHOUT_ISOLATION_F_COL, VARCOP_FAILING_HEADER)
    sheet.write(row, WITHOUT_ISOLATION_F_EXAM_COL, WITHOUT_ISOLATION_F_EXAM_HEADER)
    sheet.write(row, WITHOUT_ISOLATION_LAYER_COL, VARCOP_LAYER_HEADER)
    sheet.write(row, WITHOUT_ISOLATION_LAYER_EXAM_COL, WITHOUT_ISOLATION_LAYER_EXAM_HEADER)
    sheet.write(row, WITHOUT_ISOLATION_SPACE_COL, VARCOP_SPACE_HEADER)
    sheet.write(row, SPECTRUM_COL, SPECTRUM_HEADER)
    sheet.write(row, SPECTRUM_EXAM_COL, SPECTRUM_EXAM_HEADER)
    sheet.write(row, SPECTRUM_SPACE_COL, SPECTRUM_SPACE_HEADER)
    sheet.write(row, FEATURE_COL, FEATURE_HEADER)
    sheet.write(row, FEATURE_STM_COL, FEATURE_STM_HEADER)
    sheet.write(row, FEATURE_STM_EXAM_COL, FEATURE_STM_EXAM_HEADER)
    sheet.write(row, FEATURE_SPACE_COL, FEATURE_SPACE_HEADER)

def num_of_detected_bug(ranking_list):
    bug_count = 0
    for r in ranking_list:
        if r != -1 and r != None and type(r) != str:
            bug_count += 1
    return bug_count

def calculate_average_value_of_a_list(value_list, condition_list):
    count = 0
    sum = 0
    for i in range(0, len(value_list)):
        if value_list[i] != None and condition_list[i] != -1 and condition_list[i] != None and type(condition_list[i]) != str:
            sum += value_list[i]
            count += 1
    if count == 0:
        return 0
    return sum/count

def calculate_average_exam(value_list, condition_list):
    count = 0
    sum = 0
    for i in range(0, len(value_list)):
        if value_list[i] != None and condition_list[i] != -1 and condition_list[i] != None and type(condition_list[i]) != str:
            if(i >= 72):
                sum += value_list[i] / 143
            elif(i >= 93):
                sum += value_list[i] / 854
            elif(i >= 130):
                sum += value_list[i] / 439
            elif(i >= 182):
                sum += value_list[i] / 513
            else:
                sum += value_list[i] / 1944
            count += 1
    if count == 0:
        return 0
    return (sum / count)* 100

def calculate_average_exam(value_list, condition_list, num_of_program_stms):
    count = 0
    sum = 0
    for i in range(0, len(value_list)):
        if value_list[i] != None and condition_list[i] != -1 and condition_list[i] != None and type(condition_list[i]) != str:
            sum += value_list[i] / num_of_program_stms
            count += 1
    if count == 0:
        return 0
    return (sum / count)* 100

def calculate_average_in_a_file(experimental_file_dir, row, sheet):

    excel_data_df = pandas.read_excel(experimental_file_dir, sheet_name=None)

    for spectrum_expression_type in SPECTRUM_EXPRESSIONS_LIST:
        num_of_bugs = num_of_detected_bug(excel_data_df[spectrum_expression_type][VARCOP_SPC_FAILING_HEADER])
        sheet.write(row, NUM_DETECTED_BUGS_COL, num_of_bugs)

        sheet.write(row, SPECTRUM_EXPRESSION_COL, spectrum_expression_type)

        spc_failing_average = calculate_average_value_of_a_list(excel_data_df[spectrum_expression_type][VARCOP_SPC_FAILING_HEADER], excel_data_df[spectrum_expression_type][VARCOP_SPC_FAILING_HEADER])
        sheet.write(row, SPC_FAILING_ONLY_COL, spc_failing_average)

        spc_failing_exam = calculate_average_exam(excel_data_df[spectrum_expression_type][VARCOP_SPC_FAILING_HEADER], excel_data_df[spectrum_expression_type][VARCOP_SPC_FAILING_HEADER])
        sheet.write(row, SPC_FAILING_ONLY_EXAM_COL, spc_failing_exam)

        spc_layer_average = calculate_average_value_of_a_list(
            excel_data_df[spectrum_expression_type][VARCOP_SPC_LAYER_HEADER],
            excel_data_df[spectrum_expression_type][VARCOP_SPC_FAILING_HEADER])
        sheet.write(row, SPC_LAYER_COL, spc_layer_average)


        spc_layer_exam = calculate_average_exam(excel_data_df[spectrum_expression_type][VARCOP_SPC_LAYER_HEADER], excel_data_df[spectrum_expression_type][VARCOP_SPC_FAILING_HEADER])
        sheet.write(row, SPC_LAYER_EXAM_COL, spc_layer_exam)

        spc_space = calculate_average_value_of_a_list(
            excel_data_df[spectrum_expression_type][VARCOP_SPC_SPACE_HEADER],
            excel_data_df[spectrum_expression_type][VARCOP_SPC_FAILING_HEADER])
        sheet.write(row, SPC_SPACE_COL, spc_space)

        without_isolation_average = calculate_average_value_of_a_list(
            excel_data_df[spectrum_expression_type][VARCOP_FAILING_HEADER],
            excel_data_df[spectrum_expression_type][VARCOP_SPC_FAILING_HEADER])
        sheet.write(row, WITHOUT_ISOLATION_F_COL, without_isolation_average)

        without_isolation_exam = calculate_average_exam(excel_data_df[spectrum_expression_type][VARCOP_FAILING_HEADER], excel_data_df[spectrum_expression_type][VARCOP_SPC_FAILING_HEADER])
        sheet.write(row, WITHOUT_ISOLATION_F_EXAM_COL, without_isolation_exam)

        without_isolation_layer_average = calculate_average_value_of_a_list(
            excel_data_df[spectrum_expression_type][VARCOP_LAYER_HEADER],
            excel_data_df[spectrum_expression_type][VARCOP_SPC_FAILING_HEADER])
        sheet.write(row, WITHOUT_ISOLATION_LAYER_COL, without_isolation_layer_average)

        without_isolation_layer_exam = calculate_average_exam(excel_data_df[spectrum_expression_type][VARCOP_LAYER_HEADER], excel_data_df[spectrum_expression_type][VARCOP_SPC_FAILING_HEADER])
        sheet.write(row, WITHOUT_ISOLATION_LAYER_EXAM_COL, without_isolation_layer_exam)

        without_isolation_space = calculate_average_value_of_a_list(
            excel_data_df[spectrum_expression_type][VARCOP_SPACE_HEADER],
            excel_data_df[spectrum_expression_type][VARCOP_SPC_FAILING_HEADER])
        sheet.write(row, WITHOUT_ISOLATION_SPACE_COL, without_isolation_space)


        spectrum_average = calculate_average_value_of_a_list(
            excel_data_df[spectrum_expression_type][SPECTRUM_HEADER],
            excel_data_df[spectrum_expression_type][VARCOP_SPC_FAILING_HEADER])
        sheet.write(row, SPECTRUM_COL, spectrum_average)

        spectrum_exam = calculate_average_exam(excel_data_df[spectrum_expression_type][SPECTRUM_HEADER], excel_data_df[spectrum_expression_type][VARCOP_SPC_FAILING_HEADER])
        sheet.write(row, SPECTRUM_EXAM_COL, spectrum_exam)

        spectrum_space = calculate_average_value_of_a_list(
            excel_data_df[spectrum_expression_type][SPECTRUM_SPACE_HEADER],
            excel_data_df[spectrum_expression_type][VARCOP_SPC_FAILING_HEADER])
        sheet.write(row, SPECTRUM_SPACE_COL, spectrum_space)

        feature_average = calculate_average_value_of_a_list(
            excel_data_df[spectrum_expression_type][FEATURE_HEADER],
            excel_data_df[spectrum_expression_type][VARCOP_SPC_FAILING_HEADER])
        sheet.write(row, FEATURE_COL, feature_average)

        feature_stm_average = calculate_average_value_of_a_list(
            excel_data_df[spectrum_expression_type][FEATURE_STM_HEADER],
            excel_data_df[spectrum_expression_type][VARCOP_SPC_FAILING_HEADER])
        sheet.write(row, FEATURE_STM_COL, feature_stm_average)

        feature_stm_exam = calculate_average_exam(excel_data_df[spectrum_expression_type][FEATURE_STM_HEADER], excel_data_df[spectrum_expression_type][VARCOP_SPC_FAILING_HEADER])
        sheet.write(row, FEATURE_STM_EXAM_COL, feature_stm_exam)

        feature_space = calculate_average_value_of_a_list(
            excel_data_df[spectrum_expression_type][FEATURE_SPACE_HEADER],
            excel_data_df[spectrum_expression_type][VARCOP_SPC_FAILING_HEADER])
        sheet.write(row, FEATURE_SPACE_COL, feature_space)

        row += 1
    return row

def summary_for_same_bugs(summary_file_dir, files_list, num_of_program_stms):

    wb = Workbook(summary_file_dir)
    sheet = wb.add_worksheet("sheet1")

    row = 0
    write_header_in_sumary_file(row, sheet)
    row += 1

    overall_info = {}
    for file in files_list.keys():
        excel_data = pandas.read_excel(files_list[file], sheet_name=None)
        overall_info[file] = excel_data

    for spectrum_expression_type in SPECTRUM_EXPRESSIONS_LIST:
        for file in overall_info.keys():
            data = overall_info[file]
            data[spectrum_expression_type] = data[spectrum_expression_type][data[spectrum_expression_type][VARCOP_SPC_FAILING_HEADER] != -1]
            overall_info[file] = data

    for spectrum_expression_type in SPECTRUM_EXPRESSIONS_LIST:
        for file in overall_info.keys():
            data = overall_info[file]
            for bug in data[spectrum_expression_type][MUTATED_PROJECT_HEADER]:
                for item in overall_info.keys():
                    if file != item and (bug not in list(overall_info[item][spectrum_expression_type][MUTATED_PROJECT_HEADER])) :
                        data[spectrum_expression_type] = data[spectrum_expression_type][data[spectrum_expression_type][MUTATED_PROJECT_HEADER] != bug]
            overall_info[file] = data
        print(overall_info)

    for file in overall_info.keys():
        sheet.write(row, K_WISE_COL, file)
        data = overall_info[file]
        for spectrum_expression_type in SPECTRUM_EXPRESSIONS_LIST:
            num_of_bugs = num_of_detected_bug(data[spectrum_expression_type][VARCOP_SPC_FAILING_HEADER])
            sheet.write(row, NUM_DETECTED_BUGS_COL, num_of_bugs)

            sheet.write(row, SPECTRUM_EXPRESSION_COL, spectrum_expression_type)

            spc_failing_average = calculate_average_value_of_a_list(list(data[spectrum_expression_type][VARCOP_SPC_FAILING_HEADER]), list(data[spectrum_expression_type][VARCOP_SPC_FAILING_HEADER]))
            sheet.write(row, SPC_FAILING_ONLY_COL, spc_failing_average)

            spc_failing_exam = calculate_average_exam(
                list(data[spectrum_expression_type][VARCOP_SPC_FAILING_HEADER]),
                list(data[spectrum_expression_type][VARCOP_SPC_FAILING_HEADER]), num_of_program_stms)
            sheet.write(row, SPC_FAILING_ONLY_EXAM_COL, spc_failing_exam)

            spc_layer_average = calculate_average_value_of_a_list(
                list(data[spectrum_expression_type][VARCOP_SPC_LAYER_HEADER]),
                list(data[spectrum_expression_type][VARCOP_SPC_FAILING_HEADER]))
            sheet.write(row, SPC_LAYER_COL, spc_layer_average)

            spc_layer_exam = calculate_average_exam(
                list(data[spectrum_expression_type][VARCOP_SPC_LAYER_HEADER]),
                list(data[spectrum_expression_type][VARCOP_SPC_FAILING_HEADER]), num_of_program_stms)
            sheet.write(row, SPC_LAYER_EXAM_COL, spc_layer_exam)

            spc_space = calculate_average_value_of_a_list(
                list(data[spectrum_expression_type][VARCOP_SPC_SPACE_HEADER]),
                list(data[spectrum_expression_type][VARCOP_SPC_FAILING_HEADER]))
            sheet.write(row, SPC_SPACE_COL, spc_space)

            without_isolation_average = calculate_average_value_of_a_list(
                list(data[spectrum_expression_type][VARCOP_FAILING_HEADER]),
                list(data[spectrum_expression_type][VARCOP_SPC_FAILING_HEADER]))
            sheet.write(row, WITHOUT_ISOLATION_F_COL, without_isolation_average)

            without_isolation_exam = calculate_average_exam(
                list(data[spectrum_expression_type][VARCOP_FAILING_HEADER]),
                list(data[spectrum_expression_type][VARCOP_SPC_FAILING_HEADER]), num_of_program_stms)
            sheet.write(row, WITHOUT_ISOLATION_F_EXAM_COL, without_isolation_exam)

            without_isolation_layer_average = calculate_average_value_of_a_list(
                list(data[spectrum_expression_type][VARCOP_LAYER_HEADER]),
                list(data[spectrum_expression_type][VARCOP_SPC_FAILING_HEADER]))
            sheet.write(row, WITHOUT_ISOLATION_LAYER_COL, without_isolation_layer_average)

            without_isolation_layer_exam = calculate_average_exam(
                list(data[spectrum_expression_type][VARCOP_LAYER_HEADER]),
                list(data[spectrum_expression_type][VARCOP_SPC_FAILING_HEADER]), num_of_program_stms)
            sheet.write(row, WITHOUT_ISOLATION_LAYER_EXAM_COL, without_isolation_layer_exam)

            without_isolation_space = calculate_average_value_of_a_list(
                list(data[spectrum_expression_type][VARCOP_SPACE_HEADER]),
                list(data[spectrum_expression_type][VARCOP_SPC_FAILING_HEADER]))
            sheet.write(row, WITHOUT_ISOLATION_SPACE_COL, without_isolation_space)

            spectrum_average = calculate_average_value_of_a_list(
                list(data[spectrum_expression_type][SPECTRUM_HEADER]),
                list(data[spectrum_expression_type][VARCOP_SPC_FAILING_HEADER]))
            sheet.write(row, SPECTRUM_COL, spectrum_average)

            spectrum_exam = calculate_average_exam(
                list(data[spectrum_expression_type][SPECTRUM_HEADER]),
                list(data[spectrum_expression_type][VARCOP_SPC_FAILING_HEADER]), num_of_program_stms)
            sheet.write(row, SPECTRUM_EXAM_COL, spectrum_exam)

            spectrum_space = calculate_average_value_of_a_list(
                list(data[spectrum_expression_type][SPECTRUM_SPACE_HEADER]),
                list(data[spectrum_expression_type][VARCOP_SPC_FAILING_HEADER]))
            sheet.write(row, SPECTRUM_SPACE_COL, spectrum_space)

            feature_average = calculate_average_value_of_a_list(
                list(data[spectrum_expression_type][FEATURE_HEADER]),
                list(data[spectrum_expression_type][VARCOP_SPC_FAILING_HEADER]))
            sheet.write(row, FEATURE_COL, feature_average)

            feature_stm_average = calculate_average_value_of_a_list(
                list(data[spectrum_expression_type][FEATURE_STM_HEADER]),
                list(data[spectrum_expression_type][VARCOP_SPC_FAILING_HEADER]))
            sheet.write(row, FEATURE_STM_COL, feature_stm_average)

            feature_stm_exam = calculate_average_exam(
                list(data[spectrum_expression_type][FEATURE_STM_HEADER]),
                list(data[spectrum_expression_type][VARCOP_SPC_FAILING_HEADER]), num_of_program_stms)
            sheet.write(row, FEATURE_STM_EXAM_COL, feature_stm_exam)

            feature_space = calculate_average_value_of_a_list(
                list(data[spectrum_expression_type][FEATURE_SPACE_HEADER]),
                list(data[spectrum_expression_type][VARCOP_SPC_FAILING_HEADER]))
            sheet.write(row, FEATURE_SPACE_COL, feature_space)

            row += 1
    wb.close()

def count_total_bugs(files_list):
    bug_list = []
    overall_info = {}

    for file in files_list.keys():
        excel_data = pandas.read_excel(files_list[file], sheet_name=None)
        overall_info[file] = excel_data

    for file in overall_info.keys():
        for bug in overall_info[file][TARANTULA][MUTATED_PROJECT_HEADER]:
            if bug not in bug_list:
                print(bug)
                bug_list.append(bug)
    return len(bug_list)


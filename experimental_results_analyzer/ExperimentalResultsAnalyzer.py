import pandas

from FileManager import join_path, EXPERIMENT_RESULT_FOLDER
from ranking.Keywords import SBFL_METRIC, NUM_DETECTED_BUGS, ISOLATION_VS_SBFL_IN_RANK, ISOLATION_VS_SBFL_IN_EXAM, \
    WITHOUT_ISOLATION_VS_SBFL_IN_RANK, WITHOUT_ISOLATION_VS_SBFL_IN_EXAM
from ranking.RankingManager import VARCOP_RANK, VARCOP_SPACE, VARCOP_DISABLE_BPC_RANK, SBFL_RANK, SPACE
from ranking.RankingResultManager import VARCOP_EXAM, VARCOP_DISABLE_BPC_EXAM, SBFL_EXAM, FB_RANK, FB_EXAM, BUG_ID
from ranking.Spectrum_Expression import JACCARD, SORENSEN_DICE, TARANTULA, OCHIAI, OP2, BARINEL, DSTAR, ROGERS_TANIMOTO, \
    AMPLE, \
    SIMPLE_MATCHING, RUSSELL_RAO, COHEN, SCOTT, ROGOT1, GEOMETRIC_MEAN, M2, WONG1, SOKAL, DICE, HUMANN, OVERLAP, ZOLTAR, \
    WONG3, WONG2, M1, ROGOT2, EUCLID, HAMMING, FLEISS, ANDERBERG, KULCZYNSKI1, KULCZYNSKI2, HARMONIC_MEAN, GOODMAN

from xlsxwriter import Workbook


SBFL_METRIC_COL = 0
NUM_DETECTED_BUGS_COL = 1
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

#comparion
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

def write_all_bugs_to_a_file(summary_file_dir, file_lists):
    print(summary_file_dir)
    writer = pandas.ExcelWriter(summary_file_dir, engine='openpyxl')

    row = 0
    for file in file_lists:

        excel_data_df = pandas.read_excel(file, sheet_name=None)
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
    sheet.write(row, NUM_DETECTED_BUGS_COL, NUM_DETECTED_BUGS)
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
    sheet.write(row, ISOLATION_VS_SBFL_IN_RANK_COL, ISOLATION_VS_SBFL_IN_RANK)
    sheet.write(row, ISOLATION_VS_SBFL_IN_EXAM_COL, ISOLATION_VS_SBFL_IN_EXAM)
    sheet.write(row, WITHOUT_ISOLATION_VS_SBFL_IN_RANK_COL, WITHOUT_ISOLATION_VS_SBFL_IN_RANK)
    sheet.write(row, WITHOUT_ISOLATION_VS_SBFL_IN_EXAM_COL, WITHOUT_ISOLATION_VS_SBFL_IN_EXAM)


def num_of_detected_bug(ranking_list):
    bug_count = 0
    for r in ranking_list:
        if r != -1 and r != None and type(r) != str:
            bug_count += 1
    return bug_count


def calculate_average_value_of_a_list(value_list):
    count = 0
    sum = 0
    for i in range(0, len(value_list)):
        if value_list[i] is not None and value_list[i] != -1 and type(value_list[i]) != str:
            sum += value_list[i]
            count += 1
    if count == 0:
        return 0
    return sum / count


def calculate_average_in_a_file(experimental_file_dir, row, sheet):
    excel_data_df = pandas.read_excel(experimental_file_dir, sheet_name=None)

    varcop_win_rank = 0
    varcop_win_exam = 0
    disabled_win_rank = 0
    disabled_win_exam = 0
    sbfl_win_varcop_rank = 0
    sbfl_win_disabled_rank = 0
    sbfl_win_varcop_exam = 0
    sbfl_win_disabled_exam = 0
    for spectrum_expression_type in SPECTRUM_EXPRESSIONS_LIST:
        num_of_bugs = num_of_detected_bug(excel_data_df[spectrum_expression_type][VARCOP_RANK])
        sheet.write(row, NUM_DETECTED_BUGS_COL, num_of_bugs)

        sheet.write(row, SBFL_METRIC_COL, spectrum_expression_type)

        varcop_rank = calculate_average_value_of_a_list(
            excel_data_df[spectrum_expression_type][VARCOP_RANK])
        sheet.write(row, VARCOP_RANK_COL, varcop_rank)

        varcop_exam = calculate_average_value_of_a_list(
            excel_data_df[spectrum_expression_type][VARCOP_EXAM])
        sheet.write(row, VARCOP_EXAM_COL, varcop_exam)

        varcop_space = calculate_average_value_of_a_list(
            excel_data_df[spectrum_expression_type][VARCOP_SPACE])
        sheet.write(row, VARCOP_SPACE_COL, varcop_space)

        varcop_disable_bpc_rank = calculate_average_value_of_a_list(
            excel_data_df[spectrum_expression_type][VARCOP_DISABLE_BPC_RANK])
        sheet.write(row, VARCOP_DISABLE_BPC_RANK_COL, varcop_disable_bpc_rank)

        varcop_disable_bpc_exam = calculate_average_value_of_a_list(
            excel_data_df[spectrum_expression_type][VARCOP_DISABLE_BPC_EXAM])
        sheet.write(row, VARCOP_DISABLE_BPC_EXAM_COL, varcop_disable_bpc_exam)

        sbfl_rank = calculate_average_value_of_a_list(
            excel_data_df[spectrum_expression_type][SBFL_RANK])
        sheet.write(row, SBFL_RANK_COL, sbfl_rank)

        sbfl_exam = calculate_average_value_of_a_list(
            excel_data_df[spectrum_expression_type][SBFL_EXAM])
        sheet.write(row, SBFL_EXAM_COL, sbfl_exam)

        fb_rank = calculate_average_value_of_a_list(
            excel_data_df[spectrum_expression_type][FB_RANK])
        sheet.write(row, FB_RANK_COL, fb_rank)

        fb_exam = calculate_average_value_of_a_list(
            excel_data_df[spectrum_expression_type][FB_EXAM])
        sheet.write(row, FB_EXAM_COL, fb_exam)

        space = calculate_average_value_of_a_list(
            excel_data_df[spectrum_expression_type][SPACE])
        sheet.write(row, SPACE_COL, space)

        #comparison

        sheet.write(row, ISOLATION_VS_SBFL_IN_RANK_COL, (sbfl_rank-varcop_rank)/sbfl_rank)
        if(((sbfl_rank - varcop_rank) / sbfl_rank) > 0):
            varcop_win_rank += 1
        elif(((sbfl_rank - varcop_rank) / sbfl_rank) < 0):
            sbfl_win_varcop_rank += 1
        sheet.write(row, ISOLATION_VS_SBFL_IN_EXAM_COL, (sbfl_exam - varcop_exam) / sbfl_exam)
        if((sbfl_exam - varcop_exam) / sbfl_exam) > 0:
            varcop_win_exam += 1
        elif((sbfl_exam - varcop_exam) / sbfl_exam) < 0:
            sbfl_win_varcop_exam += 1
        sheet.write(row, WITHOUT_ISOLATION_VS_SBFL_IN_RANK_COL, (sbfl_rank - varcop_disable_bpc_rank) / sbfl_rank)
        if((sbfl_rank - varcop_disable_bpc_rank) / sbfl_rank) > 0:
            disabled_win_rank += 1
        elif((sbfl_rank - varcop_disable_bpc_rank) / sbfl_rank) < 0:
            sbfl_win_disabled_rank += 1
        sheet.write(row, WITHOUT_ISOLATION_VS_SBFL_IN_EXAM_COL, (sbfl_exam - varcop_disable_bpc_exam) / sbfl_exam)
        if((sbfl_exam - varcop_disable_bpc_exam) / sbfl_exam) >0:
            disabled_win_exam += 1
        elif((sbfl_exam - varcop_disable_bpc_exam) / sbfl_exam) < 0:
            sbfl_win_disabled_exam += 1
        row += 1
    row += 1
    sheet.write(row, 11, "VarCop win")
    sheet.write(row, ISOLATION_VS_SBFL_IN_RANK_COL, varcop_win_rank)
    sheet.write(row, ISOLATION_VS_SBFL_IN_EXAM_COL, varcop_win_exam)
    sheet.write(row, WITHOUT_ISOLATION_VS_SBFL_IN_RANK_COL, disabled_win_rank)
    sheet.write(row, WITHOUT_ISOLATION_VS_SBFL_IN_EXAM_COL, disabled_win_exam)
    row += 1
    sheet.write(row, 11, "SBFL win")
    sheet.write(row, ISOLATION_VS_SBFL_IN_RANK_COL, sbfl_win_varcop_rank)
    sheet.write(row, ISOLATION_VS_SBFL_IN_EXAM_COL, sbfl_win_varcop_exam)
    sheet.write(row, WITHOUT_ISOLATION_VS_SBFL_IN_RANK_COL, sbfl_win_disabled_rank)
    sheet.write(row, WITHOUT_ISOLATION_VS_SBFL_IN_EXAM_COL, sbfl_win_disabled_exam)
    return row



# def summary_for_same_bugs(summary_file_dir, files_list):
#     wb = Workbook(summary_file_dir)
#     sheet = wb.add_worksheet("sheet1")
#
#     row = 0
#     write_header_in_sumary_file(row, sheet)
#     row += 1
#
#     overall_info = {}
#     for file in files_list.keys():
#         excel_data = pandas.read_excel(files_list[file], sheet_name=None)
#         overall_info[file] = excel_data
#
#     for spectrum_expression_type in SPECTRUM_EXPRESSIONS_LIST:
#         for file in overall_info.keys():
#             data = overall_info[file]
#             data[spectrum_expression_type] = data[spectrum_expression_type][
#                 data[spectrum_expression_type][VARCOP_RANK] != -1]
#             overall_info[file] = data
#
#     for spectrum_expression_type in SPECTRUM_EXPRESSIONS_LIST:
#         for file in overall_info.keys():
#             print(file)
#             data = overall_info[file]
#             for bug in data[spectrum_expression_type][BUG_ID]:
#                 for item in overall_info.keys():
#                     if file != item and (bug not in list(overall_info[item][spectrum_expression_type][BUG_ID])):
#                         data[spectrum_expression_type] = data[spectrum_expression_type][
#                             data[spectrum_expression_type][BUG_ID] != bug]
#             overall_info[file] = data
#
#     for file in overall_info.keys():
#         # sheet.write(row, K_WISE_COL, file)
#         data = overall_info[file]
#         for spectrum_expression_type in SPECTRUM_EXPRESSIONS_LIST:
#             num_of_bugs = num_of_detected_bug(data[spectrum_expression_type][VARCOP_RANK])
#             sheet.write(row, NUM_DETECTED_BUGS_COL, num_of_bugs)
#
#             sheet.write(row, SBFL_METRIC_COL, spectrum_expression_type)
#
#             varcop_rank = calculate_average_value_of_a_list(
#                 data[spectrum_expression_type][VARCOP_RANK])
#             sheet.write(row, VARCOP_RANK_COL, varcop_rank)
#
#             varcop_exam = calculate_average_value_of_a_list(
#                 data[spectrum_expression_type][VARCOP_EXAM])
#             sheet.write(row, VARCOP_EXAM_COL, varcop_exam)
#
#             varcop_space = calculate_average_value_of_a_list(
#                 data[spectrum_expression_type][VARCOP_SPACE])
#             sheet.write(row, VARCOP_SPACE_COL, varcop_space)
#
#             varcop_disable_bpc_rank = calculate_average_value_of_a_list(
#                 data[spectrum_expression_type][VARCOP_DISABLE_BPC_RANK])
#             sheet.write(row, VARCOP_DISABLE_BPC_RANK_COL, varcop_disable_bpc_rank)
#
#             varcop_disable_bpc_exam = calculate_average_value_of_a_list(
#                 data[spectrum_expression_type][VARCOP_DISABLE_BPC_EXAM])
#             sheet.write(row, VARCOP_DISABLE_BPC_EXAM_COL, varcop_disable_bpc_exam)
#
#             sbfl_rank = calculate_average_value_of_a_list(
#                 data[spectrum_expression_type][SBFL_RANK])
#             sheet.write(row, SBFL_RANK_COL, sbfl_rank)
#
#             sbfl_exam = calculate_average_value_of_a_list(
#                 data[spectrum_expression_type][SBFL_EXAM])
#             sheet.write(row, SBFL_EXAM_COL, sbfl_exam)
#
#             fb_rank = calculate_average_value_of_a_list(
#                 data[spectrum_expression_type][FB_RANK])
#             sheet.write(row, FB_RANK_COL, fb_rank)
#
#             fb_exam = calculate_average_value_of_a_list(
#                 data[spectrum_expression_type][FB_EXAM])
#             sheet.write(row, FB_EXAM_COL, fb_exam)
#
#             space = calculate_average_value_of_a_list(
#                 data[spectrum_expression_type][SPACE])
#             sheet.write(row, SPACE_COL, space)
#
#             row += 1
#     wb.close()


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

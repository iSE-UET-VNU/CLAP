import pandas

from FileManager import join_path, EXPERIMENT_RESULT_FOLDER
from xlsxwriter import Workbook

from experimental_results_analyzer.ExperimentalResultsAnalyzer import write_header_in_sumary_file, SBFL_METRIC_COL, \
    VARCOP_RANK_COL, VARCOP_EXAM_COL, VARCOP_SPACE_COL, VARCOP_DISABLE_BPC_RANK_COL, \
    VARCOP_DISABLE_BPC_EXAM_COL, FB_RANK_COL, FB_EXAM_COL, SPACE_COL, SBFL_RANK_COL, SBFL_EXAM_COL, \
    SPECTRUM_EXPRESSIONS_LIST, ISOLATION_VS_SBFL_IN_RANK_COL, ISOLATION_VS_SBFL_IN_EXAM_COL, \
    WITHOUT_ISOLATION_VS_SBFL_IN_RANK_COL, WITHOUT_ISOLATION_VS_SBFL_IN_EXAM_COL, NUM_BUGS_COL

from ranking.Keywords import VARCOP_RANK, VARCOP_EXAM, VARCOP_SPACE, VARCOP_DISABLE_BPC_RANK, VARCOP_DISABLE_BPC_EXAM, \
    SBFL_RANK, SBFL_EXAM, FB_RANK, FB_EXAM, SPACE



def assumption_summary_result(all_bugs_file, summary_file):
    summary_file_dir = join_path(EXPERIMENT_RESULT_FOLDER,
                                 summary_file)
    wb = Workbook(summary_file_dir)
    sheet = wb.add_worksheet("sheet1")

    row = 0
    write_header_in_sumary_file(row, sheet)
    row += 1
    row = assumption_calculate_average_in_a_file(all_bugs_file, row, sheet)

    wb.close()

def assumption_num_of_detected_bug(ranking_list, space):
    bug_count = 0
    for r in range(0, len(ranking_list)):
        if ranking_list[r] != -1  and ranking_list[r] <= space[r] and ranking_list[r] != None and type(ranking_list[r]) != str:
            bug_count += 1
    return bug_count

def assumption_calculate_average_value_of_a_list(value_list, condition1, condition2):
    count = 0
    sum = 0
    for i in range(0, len(value_list)):
        if value_list[i] is not None and value_list[i] != -1 and condition1[i] <= condition2[i] and type(value_list[i]) != str:
            sum += value_list[i]
            count += 1
    if count == 0:
        return 0
    return sum / count

def assumption_calculate_average_in_a_file(experimental_file_dir, row, sheet):
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
        num_of_bugs = assumption_num_of_detected_bug(excel_data_df[spectrum_expression_type][VARCOP_RANK], excel_data_df[spectrum_expression_type][VARCOP_SPACE])
        sheet.write(row, NUM_BUGS_COL, num_of_bugs)

        sheet.write(row, SBFL_METRIC_COL, spectrum_expression_type)

        varcop_rank = assumption_calculate_average_value_of_a_list(
            excel_data_df[spectrum_expression_type][VARCOP_RANK],
            excel_data_df[spectrum_expression_type][VARCOP_RANK],
            excel_data_df[spectrum_expression_type][VARCOP_SPACE])
        sheet.write(row, VARCOP_RANK_COL, varcop_rank)

        varcop_exam = assumption_calculate_average_value_of_a_list(
            excel_data_df[spectrum_expression_type][VARCOP_EXAM],
            excel_data_df[spectrum_expression_type][VARCOP_RANK],
            excel_data_df[spectrum_expression_type][VARCOP_SPACE])
        sheet.write(row, VARCOP_EXAM_COL, varcop_exam)

        varcop_space = assumption_calculate_average_value_of_a_list(
            excel_data_df[spectrum_expression_type][VARCOP_SPACE],
            excel_data_df[spectrum_expression_type][VARCOP_RANK],
            excel_data_df[spectrum_expression_type][VARCOP_SPACE])
        sheet.write(row, VARCOP_SPACE_COL, varcop_space)

        varcop_disable_bpc_rank = assumption_calculate_average_value_of_a_list(
            excel_data_df[spectrum_expression_type][VARCOP_DISABLE_BPC_RANK],
            excel_data_df[spectrum_expression_type][VARCOP_RANK],
            excel_data_df[spectrum_expression_type][VARCOP_SPACE])
        sheet.write(row, VARCOP_DISABLE_BPC_RANK_COL, varcop_disable_bpc_rank)

        varcop_disable_bpc_exam = assumption_calculate_average_value_of_a_list(
            excel_data_df[spectrum_expression_type][VARCOP_DISABLE_BPC_EXAM],
            excel_data_df[spectrum_expression_type][VARCOP_RANK],
            excel_data_df[spectrum_expression_type][VARCOP_SPACE])
        sheet.write(row, VARCOP_DISABLE_BPC_EXAM_COL, varcop_disable_bpc_exam)

        sbfl_rank = assumption_calculate_average_value_of_a_list(
            excel_data_df[spectrum_expression_type][SBFL_RANK],
            excel_data_df[spectrum_expression_type][VARCOP_RANK],
            excel_data_df[spectrum_expression_type][VARCOP_SPACE])
        sheet.write(row, SBFL_RANK_COL, sbfl_rank)

        sbfl_exam = assumption_calculate_average_value_of_a_list(
            excel_data_df[spectrum_expression_type][SBFL_EXAM],
            excel_data_df[spectrum_expression_type][VARCOP_RANK],
            excel_data_df[spectrum_expression_type][VARCOP_SPACE])
        sheet.write(row, SBFL_EXAM_COL, sbfl_exam)

        fb_rank = assumption_calculate_average_value_of_a_list(
            excel_data_df[spectrum_expression_type][FB_RANK],
            excel_data_df[spectrum_expression_type][VARCOP_RANK],
            excel_data_df[spectrum_expression_type][VARCOP_SPACE])
        sheet.write(row, FB_RANK_COL, fb_rank)

        fb_exam = assumption_calculate_average_value_of_a_list(
            excel_data_df[spectrum_expression_type][FB_EXAM],
            excel_data_df[spectrum_expression_type][VARCOP_RANK],
            excel_data_df[spectrum_expression_type][VARCOP_SPACE])
        sheet.write(row, FB_EXAM_COL, fb_exam)

        space = assumption_calculate_average_value_of_a_list(
            excel_data_df[spectrum_expression_type][SPACE],
            excel_data_df[spectrum_expression_type][VARCOP_RANK],
            excel_data_df[spectrum_expression_type][VARCOP_SPACE])
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



def assumption_summary_hitx(hitx_file_dir, all_bugs_file_dir):
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
            sheet.write(row, col, assumption_count_hit_x(excel_data_df[spectrum_expression_type][VARCOP_RANK], excel_data_df[spectrum_expression_type][VARCOP_RANK],
                                                         excel_data_df[spectrum_expression_type][VARCOP_SPACE], hit_list[index]))
            col += 1
            sheet.write(row, col,
                        assumption_count_hit_x(excel_data_df[spectrum_expression_type][SBFL_RANK],
                                               excel_data_df[spectrum_expression_type][VARCOP_RANK],
                                               excel_data_df[spectrum_expression_type][VARCOP_SPACE],
                                               hit_list[index]))
        row += 1

    wb.close()

def  assumption_count_hit_x(value_list, condition1, condition2, x):
    count = 0
    for value in range(0, len(value_list)):
        if type(value_list[value]) != str and value_list[value] != -1 and condition1[value] <= condition2[value] and value_list[value] <= x:
            count += 1
    return count
from ranking.Keywords import VARCOP_WIN_RANK, VARCOP_WIN_EXAM, VARCOP_DISABLE_BPC_WIN_RANK, VARCOP_DISABLE_BPC_WIN_EXAM, \
    SBFL_WIN_VARCOP_RANK, SBFL_WIN_VARCOP_EXAM, SBFL_WIN_VARCOP_DISABLED_BPC_RANK, SBFL_WIN_VARCOP_DISABLED_BPC_EXAM, \
    VARCOP_RANK, SBFL_RANK, VARCOP_EXAM, SBFL_EXAM, VARCOP_DISABLE_BPC_RANK, VARCOP_DISABLE_BPC_EXAM, SBFL_METRIC, \
    VARCOP_VS_SBFL_IN_RANK, VARCOP_VS_SBFL_IN_EXAM, VARCOP_DISABLE_BPC_VS_SBFL_IN_RANK, \
    VARCOP_DISABLE_BPC_VS_SBFL_IN_EXAM
from ranking.Spectrum_Expression import JACCARD, SORENSEN_DICE, TARANTULA, OCHIAI, OP2, BARINEL, DSTAR, ROGERS_TANIMOTO, \
    AMPLE, \
    SIMPLE_MATCHING, RUSSELL_RAO, COHEN, SCOTT, ROGOT1, GEOMETRIC_MEAN, M2, WONG1, SOKAL, DICE, HUMANN, OVERLAP, ZOLTAR, \
    WONG3, WONG2, M1, ROGOT2, EUCLID, HAMMING, FLEISS, ANDERBERG, KULCZYNSKI1, KULCZYNSKI2, HARMONIC_MEAN, GOODMAN

from xlsxwriter import Workbook

comparison_list = [VARCOP_WIN_RANK, VARCOP_WIN_EXAM, VARCOP_DISABLE_BPC_WIN_RANK, VARCOP_DISABLE_BPC_WIN_EXAM,
                   SBFL_WIN_VARCOP_RANK, SBFL_WIN_VARCOP_EXAM, SBFL_WIN_VARCOP_DISABLED_BPC_RANK,
                   SBFL_WIN_VARCOP_DISABLED_BPC_EXAM]

SBFL_METRIC_COL = 0
VARCOP_VS_SBFL_RANK_COL = 1
VARCOP_VS_SBFL_EXAM_COL = 2

SPECTRUM_EXPRESSIONS_LIST = [TARANTULA, OCHIAI, OP2, BARINEL, DSTAR,
                             RUSSELL_RAO, SIMPLE_MATCHING, ROGERS_TANIMOTO, AMPLE, JACCARD,
                             COHEN, SCOTT, ROGOT1, GEOMETRIC_MEAN, M2,
                             WONG1, SOKAL, SORENSEN_DICE, DICE, HUMANN, WONG2, ZOLTAR,
                             EUCLID, ROGOT2, HAMMING, FLEISS, ANDERBERG,
                             GOODMAN, HARMONIC_MEAN, KULCZYNSKI2]

def init_comparison_data():
    data = {}
    for metric in comparison_list:
        if metric not in data:
            data[metric] = 0
    return data


def comparison(data, average_value_list, spectrum_expression):
    data[spectrum_expression] = {}
    tmp = varcop_win(average_value_list[VARCOP_RANK], average_value_list[SBFL_RANK])
    data[spectrum_expression][VARCOP_VS_SBFL_IN_RANK] = tmp

    if tmp > 0:
        data[VARCOP_WIN_RANK] += 1
    elif tmp < 0:
        data[SBFL_WIN_VARCOP_RANK] += 1

    tmp = varcop_win(average_value_list[VARCOP_EXAM], average_value_list[SBFL_EXAM])
    data[spectrum_expression][VARCOP_VS_SBFL_IN_EXAM] = tmp
    if tmp > 0:
        data[VARCOP_WIN_EXAM] += 1
    elif tmp < 0:
        data[SBFL_WIN_VARCOP_EXAM] += 1

    tmp = varcop_win(average_value_list[VARCOP_DISABLE_BPC_RANK], average_value_list[SBFL_RANK])
    data[spectrum_expression][VARCOP_DISABLE_BPC_VS_SBFL_IN_RANK] = tmp
    if tmp > 0:
        data[VARCOP_DISABLE_BPC_WIN_RANK] += 1
    elif tmp < 0:
        data[SBFL_WIN_VARCOP_DISABLED_BPC_RANK] += 1

    tmp = varcop_win(average_value_list[VARCOP_DISABLE_BPC_EXAM], average_value_list[SBFL_EXAM])
    data[spectrum_expression][VARCOP_DISABLE_BPC_VS_SBFL_IN_EXAM] = tmp
    if tmp > 0:
        data[VARCOP_DISABLE_BPC_WIN_EXAM] += 1
    elif tmp < 0:
        data[SBFL_WIN_VARCOP_DISABLED_BPC_EXAM] += 1

    return data


def varcop_win(varcop, sbfl):
    return (sbfl - varcop)/sbfl

def write_result_varcop_vs_sbfl(sheet, comparison_data):
    systems = list(comparison_data.keys())
    row = 1
    sheet.write(row, 0, "SPFL Metric")
    row += 1
    for spectrum_expression in SPECTRUM_EXPRESSIONS_LIST:
        sheet.write(row, 0, spectrum_expression)
        row+= 1
    sheet.write(row, 0, "VarCop win")
    row += 1
    sheet.write(row, 0, "SBFL win")
    for index in range(0, len(systems)):
        row = 0
        sheet.write(row, 2*index + 1, systems[index])
        row += 1
        sheet.write(row, 2*index + 1, "RANK")
        sheet.write(row, 2*index + 2, "EXAM")
        row += 1
        for spectrum_expression in SPECTRUM_EXPRESSIONS_LIST:
            sheet.write(row, 2*index + 1, comparison_data[systems[index]][spectrum_expression][VARCOP_VS_SBFL_IN_RANK])
            sheet.write(row, 2*index + 2, comparison_data[systems[index]][spectrum_expression][VARCOP_VS_SBFL_IN_EXAM])
            row += 1
        sheet.write(row, 2*index + 1, comparison_data[systems[index]][VARCOP_WIN_RANK])
        sheet.write(row, 2*index + 2, comparison_data[systems[index]][VARCOP_WIN_EXAM])
        row += 1
        sheet.write(row, 2*index + 1, comparison_data[systems[index]][SBFL_WIN_VARCOP_RANK])
        sheet.write(row, 2*index + 2, comparison_data[systems[index]][SBFL_WIN_VARCOP_EXAM])

def write_result_varcop_disabled_bpc_vs_sbfl(sheet, comparison_data):
    systems = list(comparison_data.keys())
    row = 1
    sheet.write(row, 0, "SPFL Metric")
    row += 1
    for spectrum_expression in SPECTRUM_EXPRESSIONS_LIST:
        sheet.write(row, 0, spectrum_expression)
        row+= 1
    sheet.write(row, 0, "VarCop win")
    row += 1
    sheet.write(row, 0, "SBFL win")
    for index in range(0, len(systems)):
        row = 0
        sheet.write(row, 2*index + 1, systems[index])
        row += 1
        sheet.write(row, 2*index + 1, "RANK")
        sheet.write(row, 2*index + 2, "EXAM")
        row += 1
        for spectrum_expression in SPECTRUM_EXPRESSIONS_LIST:
            sheet.write(row, 2*index + 1, comparison_data[systems[index]][spectrum_expression][VARCOP_DISABLE_BPC_VS_SBFL_IN_RANK])
            sheet.write(row, 2*index + 2, comparison_data[systems[index]][spectrum_expression][VARCOP_DISABLE_BPC_VS_SBFL_IN_EXAM])
            row += 1
        sheet.write(row, 2*index + 1, comparison_data[systems[index]][VARCOP_DISABLE_BPC_WIN_RANK])
        sheet.write(row, 2*index + 2, comparison_data[systems[index]][VARCOP_DISABLE_BPC_WIN_EXAM])
        row += 1
        sheet.write(row, 2*index + 1, comparison_data[systems[index]][SBFL_WIN_VARCOP_DISABLED_BPC_RANK])
        sheet.write(row, 2*index + 2, comparison_data[systems[index]][SBFL_WIN_VARCOP_DISABLED_BPC_EXAM])

def write_comparison_data_to_file(file_path, comparison_data):
    wb = Workbook(file_path)
    sheet = wb.add_worksheet("VARCOP")
    sheet2 = wb.add_worksheet("VARCOP DISABLED BPC")
    write_result_varcop_vs_sbfl(sheet, comparison_data)
    write_result_varcop_disabled_bpc_vs_sbfl(sheet2, comparison_data)
    wb.close()
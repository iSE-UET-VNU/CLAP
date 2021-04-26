import pandas

from ranking.RankingManager import VARCOP_RANK, SBFL_RANK
from ranking.RankingResultManager import BUG_ID

MAX = 100000
MIN = -100000


def sbfl_only_percentage_of_bugs_found(multiple_bugs_file, sbfl_metric, examined_statements):
    excel_data_df = pandas.read_excel(multiple_bugs_file, sheet_name=None)
    results = {}
    for num in range(0, 31):
        sum_sbfl = 0
        num_of_cases = 0
        count = 0
        for i in range(0, len(excel_data_df[sbfl_metric][BUG_ID])):
            if (excel_data_df[sbfl_metric][BUG_ID][i] != BUG_ID and not pandas.isnull(
                    excel_data_df[sbfl_metric][BUG_ID][i])):
                if count != 0:
                    sum_sbfl += sbpl / count
                    num_of_cases += 1
                sbpl = 0
                count = 0

            sbfl_rank = excel_data_df[sbfl_metric]["SBFL:RANK"][i]

            if (type(sbfl_rank) == int and sbfl_rank != -1 and sbfl_rank <= num):
                sbpl += 1
            if excel_data_df[sbfl_metric][BUG_ID][i] != BUG_ID:
                count += 1
        if (count != 0):
            sum_sbfl += sbpl / count
            num_of_cases += 1
        results[num] = {}
        results[num]["sbfl"] = sum_sbfl / num_of_cases
    return results


def sbfl_only_average_best_rank(multiple_bugs_file, sbfl_metric):
    excel_data_df = pandas.read_excel(multiple_bugs_file, sheet_name=None)

    tmp_sbfl = MAX

    sum_sbfl = 0
    num_of_cases = 0
    for i in range(0, len(excel_data_df[sbfl_metric][BUG_ID])):
        if (excel_data_df[sbfl_metric][BUG_ID][i] != BUG_ID and not pandas.isnull(
                excel_data_df[sbfl_metric][BUG_ID][i])):
            if tmp_sbfl != MAX:
                sum_sbfl += tmp_sbfl
                num_of_cases += 1

            tmp_sbfl = MAX

        sbfl_rank = excel_data_df[sbfl_metric]["SBFL:RANK"][i]
        if type(sbfl_rank) == int and sbfl_rank < tmp_sbfl:
            tmp_sbfl = sbfl_rank

    # print("varcop", sum_varcop/num_of_cases)
    # print("sbfl", sum_sbfl/num_of_cases)
    if tmp_sbfl != MAX:
        sum_sbfl += tmp_sbfl
        num_of_cases += 1
    # print("sum", sum_sbfl)
    # print("num of cases", num_of_cases)
    return sum_sbfl / num_of_cases


def sbfl_only_average_worst_rank(multiple_bugs_file, sbfl_metric):
    excel_data_df = pandas.read_excel(multiple_bugs_file, sheet_name=None)
    tmp_sbfl = MIN
    sum_sbfl = 0
    num_of_cases = 0
    for i in range(0, len(excel_data_df[sbfl_metric][BUG_ID])):
        if excel_data_df[sbfl_metric][BUG_ID][i] != BUG_ID and not pandas.isnull(excel_data_df[sbfl_metric][BUG_ID][i]):
            if (tmp_sbfl != MIN):
                sum_sbfl += tmp_sbfl
                num_of_cases += 1

            tmp_sbfl = MIN

        sbfl_rank = excel_data_df[sbfl_metric]["SBFL:RANK"][i]

        if (type(sbfl_rank) == int and sbfl_rank > tmp_sbfl):
            tmp_sbfl = sbfl_rank

    # print("varcop", sum_varcop/num_of_cases)
    # print("sbfl", sum_sbfl/num_of_cases)
    if (tmp_sbfl != MIN):
        sum_sbfl += tmp_sbfl
        num_of_cases += 1
    return sum_sbfl / num_of_cases

def sbfl_only_average_best_exam(multiple_bugs_file, sbfl_metric):
    excel_data_df = pandas.read_excel(multiple_bugs_file, sheet_name=None)

    tmp_sbfl = MAX

    sum_sbfl = 0
    num_of_cases = 0
    for i in range(0, len(excel_data_df[sbfl_metric][BUG_ID])):
        if (excel_data_df[sbfl_metric][BUG_ID][i] != BUG_ID and not pandas.isnull(
                excel_data_df[sbfl_metric][BUG_ID][i])):
            if tmp_sbfl != MAX:
                sum_sbfl += tmp_sbfl
                num_of_cases += 1

            tmp_sbfl = MAX

        sbfl_rank = excel_data_df[sbfl_metric]["SBFL:EXAM"][i]
        if type(sbfl_rank) != str and sbfl_rank < tmp_sbfl:
            tmp_sbfl = sbfl_rank

    # print("varcop", sum_varcop/num_of_cases)
    # print("sbfl", sum_sbfl/num_of_cases)
    if tmp_sbfl != MAX:
        sum_sbfl += tmp_sbfl
        num_of_cases += 1
    # print("sum", sum_sbfl)
    # print("num of cases", num_of_cases)
    return sum_sbfl / num_of_cases


def sbfl_only_average_worst_exam(multiple_bugs_file, sbfl_metric):
    excel_data_df = pandas.read_excel(multiple_bugs_file, sheet_name=None)
    tmp_sbfl = MIN
    sum_sbfl = 0
    num_of_cases = 0
    for i in range(0, len(excel_data_df[sbfl_metric][BUG_ID])):
        if excel_data_df[sbfl_metric][BUG_ID][i] != BUG_ID and not pandas.isnull(excel_data_df[sbfl_metric][BUG_ID][i]):
            if (tmp_sbfl != MIN):
                sum_sbfl += tmp_sbfl
                num_of_cases += 1

            tmp_sbfl = MIN

        sbfl_rank = excel_data_df[sbfl_metric]["SBFL:EXAM"][i]

        if (type(sbfl_rank) != str and sbfl_rank > tmp_sbfl):
            tmp_sbfl = sbfl_rank

    # print("varcop", sum_varcop/num_of_cases)
    # print("sbfl", sum_sbfl/num_of_cases)
    if (tmp_sbfl != MIN):
        sum_sbfl += tmp_sbfl
        num_of_cases += 1
    return sum_sbfl / num_of_cases


def sbfl_only_num_of_case_found_bugs(multiple_bugs_file, sbfl_metric, examined_statements):
    excel_data_df = pandas.read_excel(multiple_bugs_file, sheet_name=None)
    results = {}
    for num in range(0, 31):
        sum_sbfl = 0
        num_of_cases = 0
        count = 0
        for i in range(0, len(excel_data_df[sbfl_metric][BUG_ID])):
            if (excel_data_df[sbfl_metric][BUG_ID][i] != BUG_ID and not pandas.isnull(
                    excel_data_df[sbfl_metric][BUG_ID][i])):
                if count != 0:
                    if sbpl >= 1:
                        sum_sbfl += 1
                    num_of_cases += 1
                sbpl = 0
                count = 0

            sbfl_rank = excel_data_df[sbfl_metric]["SBFL:RANK"][i]

            if type(sbfl_rank) == int and sbfl_rank != -1 and sbfl_rank <= num:
                sbpl += 1
            count += 1
        if count != 0:
            if sbpl >= 1:
                sum_sbfl += 1
            num_of_cases += 1
        results[num] = {}
        results[num]["sbfl"] = sum_sbfl / num_of_cases
        results[num]["hitx"] = sum_sbfl
    return results

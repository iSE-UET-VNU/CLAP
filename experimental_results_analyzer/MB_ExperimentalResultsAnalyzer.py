import pandas

from ranking.RankingManager import VARCOP_RANK, SBFL_RANK
from ranking.RankingResultManager import BUG_ID

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
            if(excel_data_df[sbfl_metric][BUG_ID][i] != BUG_ID and  not pandas.isnull(excel_data_df[sbfl_metric][BUG_ID][i])):
                if(count != 0):
                    sum_varcop += varcop/count
                    sum_sbfl += sbpl/count
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
        results[num]["varcop"] = sum_varcop/num_of_cases
        results[num]["sbfl"] = sum_sbfl/num_of_cases
    return results

def average_best_rank(multiple_bugs_file, sbfl_metric):
    excel_data_df = pandas.read_excel(multiple_bugs_file, sheet_name=None)
    tmp_varcop = MAX
    tmp_sbfl = MAX
    sum_varcop = 0
    sum_sbfl = 0
    num_of_cases = 0
    for i in range(0, len(excel_data_df[sbfl_metric][BUG_ID])):
        if(excel_data_df[sbfl_metric][BUG_ID][i] != BUG_ID and  not pandas.isnull(excel_data_df[sbfl_metric][BUG_ID][i])):
            if(tmp_varcop != MAX and tmp_sbfl != MAX):
                sum_varcop += tmp_varcop
                sum_sbfl += tmp_sbfl
                num_of_cases += 1
            tmp_varcop = MAX
            tmp_sbfl = MAX

        varcop_rank = excel_data_df[sbfl_metric]["VARCOP:RANK"][i]
        sbfl_rank = excel_data_df[sbfl_metric]["SBFL:RANK"][i]

        if type(varcop_rank) == int and varcop_rank < tmp_varcop:
            tmp_varcop = varcop_rank
        if type(sbfl_rank) == int and sbfl_rank < tmp_sbfl:
            tmp_sbfl = sbfl_rank

    #print("varcop", sum_varcop/num_of_cases)
    #print("sbfl", sum_sbfl/num_of_cases)
    return sum_varcop/num_of_cases, sum_sbfl/num_of_cases

def average_worst_rank(multiple_bugs_file, sbfl_metric):
    excel_data_df = pandas.read_excel(multiple_bugs_file, sheet_name=None)
    tmp_varcop = MIN
    tmp_sbfl = MIN
    sum_varcop = 0
    sum_sbfl = 0
    num_of_cases = 0
    for i in range(0, len(excel_data_df[sbfl_metric][BUG_ID])):
        if excel_data_df[sbfl_metric][BUG_ID][i] != BUG_ID and  not pandas.isnull(excel_data_df[sbfl_metric][BUG_ID][i]):
            if(tmp_varcop != MIN and tmp_sbfl != MIN):
                sum_varcop += tmp_varcop
                sum_sbfl += tmp_sbfl
                num_of_cases += 1
            tmp_varcop = MIN
            tmp_sbfl = MIN

        varcop_rank = excel_data_df[sbfl_metric]["VARCOP:RANK"][i]
        sbfl_rank = excel_data_df[sbfl_metric]["SBFL:RANK"][i]

        if (type(varcop_rank) == int and varcop_rank > tmp_varcop):
            tmp_varcop = varcop_rank
        if (type(sbfl_rank) == int and sbfl_rank > tmp_sbfl):
            tmp_sbfl = sbfl_rank

    #print("varcop", sum_varcop/num_of_cases)
    #print("sbfl", sum_sbfl/num_of_cases)
    return sum_varcop/num_of_cases, sum_sbfl/num_of_cases

def num_of_case_found_bugs(multiple_bugs_file, sbfl_metric, examined_statements):
    excel_data_df = pandas.read_excel(multiple_bugs_file, sheet_name=None)
    results = {}
    for num in examined_statements:
        sum_varcop = 0
        sum_sbfl = 0
        num_of_cases = 0
        count = 0
        for i in range(0, len(excel_data_df[sbfl_metric][BUG_ID])):
            if(excel_data_df[sbfl_metric][BUG_ID][i] != BUG_ID and  not pandas.isnull(excel_data_df[sbfl_metric][BUG_ID][i])):
                if(count != 0):
                    if(varcop >= 1):
                        sum_varcop += 1
                    if(sbpl >= 1):
                        sum_sbfl += 1
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
        results[num]["varcop"] = sum_varcop/num_of_cases
        results[num]["sbfl"] = sum_sbfl/num_of_cases
    return results
import os

from xlsxwriter import Workbook

from ranking import RankingManager
from ranking.FeaturesRankingManager import features_ranking_multiple_bugs
from ranking.Keywords import VARCOP_DISABLE_BPC_RANK, VARCOP_DISABLE_BPC_EXAM, FB_RANK, FB_EXAM, BUG_ID, BUGGY_STM, \
    VARCOP_EXAM, SBFL_EXAM
from ranking.RankingManager import VARCOP_RANK, SBFL_RANK, \
    ranking_multiple_bugs, VARCOP_SPACE, SPACE
from FileManager import join_path, EXPERIMENT_RESULT_FOLDER, get_mutated_projects_dir, list_dir, get_spc_log_file_path, \
    get_project_sub_dir_by_folder_name
from ranking.VarBugManager import is_var_bug, is_var_bug_by_config
from spc import SPCsManager
from suspicious_statements_manager import SlicingManager
from suspicious_statements_manager.SuspiciousStatementManager import get_multiple_buggy_statements, \
    get_suspicious_statement

BUG_ID_COL = 0
VARCOP_BUGGY_STM_COL = 1
VARCOP_RANK_COL = 2
VARCOP_EXAM_COL = 3
VARCOP_SPACE_COL = 4
VARCOP_DISABLE_BPC_RANK_COL = 5
VARCOP_DISABLE_BPC_EXAM_COL = 6
SBFL_RANK_COL = 7
SBFL_EXAM_COL = 8
FB_RANK_COL = 9
FB_EXAM_COL = 10
SBFL_SPACE_COL = 11
IS_VAR_BUG_COL = 12


def write_header_in_result_file(row, sheet):
    sheet.write(row, BUG_ID_COL, BUG_ID)
    sheet.write(row, VARCOP_BUGGY_STM_COL, BUGGY_STM)
    sheet.write(row, VARCOP_RANK_COL, VARCOP_RANK)
    sheet.write(row, VARCOP_EXAM_COL, VARCOP_EXAM)
    sheet.write(row, VARCOP_SPACE_COL, VARCOP_SPACE)
    sheet.write(row, VARCOP_DISABLE_BPC_RANK_COL, VARCOP_DISABLE_BPC_RANK)
    sheet.write(row, VARCOP_DISABLE_BPC_EXAM_COL, VARCOP_DISABLE_BPC_EXAM)
    sheet.write(row, SBFL_RANK_COL, SBFL_RANK)
    sheet.write(row, SBFL_EXAM_COL, SBFL_EXAM)
    sheet.write(row, FB_RANK_COL, FB_RANK)
    sheet.write(row, FB_EXAM_COL, FB_EXAM)
    sheet.write(row, SBFL_SPACE_COL, SPACE)
    sheet.write(row, IS_VAR_BUG_COL, "IS_VAR_BUG")


def write_result_to_file(row, sheet, ranking_results, fb_results, space, is_var_bug):

    for stm in ranking_results[VARCOP_RANK].keys():
        sheet.write(row, VARCOP_BUGGY_STM_COL, stm)

        if(is_var_bug):
            sheet.write(row, VARCOP_RANK_COL, ranking_results[VARCOP_RANK][stm])
            exam = (ranking_results[VARCOP_RANK][stm] / space[SBFL_RANK]) * 100
            sheet.write(row, VARCOP_EXAM_COL, exam)
            sheet.write(row, VARCOP_SPACE_COL, space[VARCOP_RANK])
        else:
            sheet.write(row, VARCOP_RANK_COL, ranking_results[VARCOP_DISABLE_BPC_RANK][stm])
            exam = (ranking_results[VARCOP_DISABLE_BPC_RANK][stm] / space[SBFL_RANK]) * 100
            sheet.write(row, VARCOP_EXAM_COL, exam)

            sheet.write(row, VARCOP_SPACE_COL, space[SBFL_RANK])
            sheet.write(row, IS_VAR_BUG_COL, 0)

        sheet.write(row, VARCOP_DISABLE_BPC_RANK_COL, ranking_results[VARCOP_DISABLE_BPC_RANK][stm])
        disabled_bpc_exam = (ranking_results[VARCOP_DISABLE_BPC_RANK][stm] / space[SBFL_RANK]) * 100
        sheet.write(row, VARCOP_DISABLE_BPC_EXAM_COL, disabled_bpc_exam)

        sheet.write(row, SBFL_RANK_COL, ranking_results[SBFL_RANK][stm])
        sheet.write(row, SBFL_EXAM_COL, (ranking_results[SBFL_RANK][stm] / space[SBFL_RANK]) * 100)

        sheet.write(row, FB_RANK_COL, fb_results[stm])
        sheet.write(row, FB_EXAM_COL, (fb_results[stm] / space[SBFL_RANK]) * 100)

        sheet.write(row, SBFL_SPACE_COL, space[SBFL_RANK])
        row += 1
    return row


def multiple_bugs_ranking(result_folder, system_name, bug_folder, system_dir, kwise, spectrum_expressions, filtering_coverage_rate, coverage_version, alpha):
    aggregations = [RankingManager.AGGREGATION_ARITHMETIC_MEAN]
    normalizations = [RankingManager.NORMALIZATION_ALPHA_BETA]


    mutated_projects_dir = join_path(system_dir, kwise)
    print(mutated_projects_dir)
    if(os.path.exists(mutated_projects_dir)):
        mutated_projects = list_dir(mutated_projects_dir)

        result_folder_dir = join_path(EXPERIMENT_RESULT_FOLDER, result_folder)
        if not os.path.exists(result_folder_dir):
            os.makedirs(result_folder_dir)

        system_result_dir = join_path(result_folder_dir, system_name)
        if not os.path.exists(system_result_dir):
            os.makedirs(system_result_dir)


        for normalization_type in normalizations:
            normalization_result_dir = join_path(system_result_dir, normalization_type)
            if not os.path.exists(normalization_result_dir):
                os.makedirs(normalization_result_dir)

            for aggregation_type in aggregations:
                aggregation_result_dir = join_path(normalization_result_dir, aggregation_type)
                if not os.path.exists(aggregation_result_dir):
                    os.makedirs(aggregation_result_dir)

                kwise_result_dir = join_path(aggregation_result_dir, kwise)
                if not os.path.exists(kwise_result_dir):
                    os.makedirs(kwise_result_dir)

                sheet = []

                row = 0

                experiment_file_name = join_path(kwise_result_dir,
                                                 bug_folder + coverage_version +  ".xlsx")
                # if os.path.exists(experiment_file_name):
                #     continue
                wb = Workbook(experiment_file_name)

                for i in range(0, len(spectrum_expressions)):
                    sheet.append(wb.add_worksheet(spectrum_expressions[i]))
                    write_header_in_result_file(row, sheet[i])
                row += 1
                num_of_bugs = 0
                runtime = {}
                for mutated_project_name in mutated_projects:
                    print(mutated_project_name)
                    num_of_bugs += 1
                    mutated_project_dir = join_path(mutated_projects_dir, mutated_project_name)
                    # spc_log_file_path, spc_runtime = SPCsManager.find_SPCs(mutated_project_dir, filtering_coverage_rate)
                    #
                    # spc_log_file_path = get_spc_log_file_path(mutated_project_dir, filtering_coverage_rate)
                    # slicing_runtime = SlicingManager.do_slice(spc_log_file_path, filtering_coverage_rate, coverage_version)
                    if(coverage_version == ""):
                        suspicious_stms_list = get_suspicious_statement(mutated_project_dir, filtering_coverage_rate)
                    else:
                        post_fix = str(filtering_coverage_rate) + "_" + coverage_version + "_"
                        suspicious_stms_list = get_suspicious_statement(mutated_project_dir, post_fix)

                    buggy_statements = get_multiple_buggy_statements(mutated_project_name, mutated_project_dir)


                    row_temp = row
                    varcop_ranking_time = 0

                    if(system_name == "ZipMe"):
                        is_a_var_bug = is_var_bug_by_config(mutated_project_dir, ["Base", "Compress"])
                    else:
                        is_a_var_bug = is_var_bug_by_config(mutated_project_dir, ["Base"])

                    ranking_results, space, varcop_ranking_time = ranking_multiple_bugs(buggy_statements, mutated_project_dir,
                                                                   suspicious_stms_list,
                                                                       spectrum_expressions,
                                                                       aggregation_type,
                                                                       normalization_type, coverage_version, filtering_coverage_rate, alpha)
                    fb_ranking_results = features_ranking_multiple_bugs(buggy_statements, mutated_project_dir,
                                                                filtering_coverage_rate, spectrum_expressions)
                        #
                    for sbfl_expression in range(0, len(spectrum_expressions)):
                        sheet[sbfl_expression].write(row_temp, BUG_ID_COL, mutated_project_name)
                        row = write_result_to_file(row_temp, sheet[sbfl_expression], ranking_results[spectrum_expressions[sbfl_expression]],
                                                   fb_ranking_results[spectrum_expressions[sbfl_expression]],
                                                   space[spectrum_expressions[sbfl_expression]], is_a_var_bug)
                    #runtime[mutated_project_name] = [spc_runtime, slicing_runtime, varcop_ranking_time]
                #write_runtime_to_file(system_result_dir, runtime, "multiple_bug_runtime.xlsx")

                wb.close()

def write_runtime_to_file(system_result_dir, run_time, file_name):
    experiment_file_name = join_path(system_result_dir,
                                     file_name)
    if os.path.exists(experiment_file_name):
        return
    wb = Workbook(experiment_file_name)
    sheet = wb.add_worksheet("run_time")
    row = 0
    for item in run_time.keys():
        sheet.write(row, 0, item)
        col = 1
        for time in run_time[item]:
            sheet.write(row, col, time)
            col += 1
        row += 1
    wb.close()

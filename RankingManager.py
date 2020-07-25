import logging
import math
import os
import time
import xml.etree.ElementTree as ET

from FileManager import join_path, SPECTRUM_FAILED_COVERAGE_FILE_NAME, SPECTRUM_PASSED_COVERAGE_FILE_NAME, \
    get_test_coverage_dir, PASSED_TEST_COVERAGE_FOLDER_NAME, FAILED_TEST_COVERAGE_FOLDER_NAME, get_variant_dir, \
    get_variants_dir

# keywords
from Spectrum_Expression import tarantula_calculation, ochiai_calculation, op2_calculation, barinel_calculation, \
    dstar_calculation, TARANTULA_SCORE, TARANTULA, OCHIAI, OCHIAI_SCORE, OP2_SCORE, OP2, BARINEL, BARINEL_SCORE, DSTAR, \
    DSTAR_SCORE

FAILED_TEST_COUNT = 'failed_test_count'
PASSED_TEST_COUNT = 'passed_test_count'
SUSPICIOUS = 'suspicious'
COUNT = "count"
PASSING_COUNT = "passing_count"

RANKING_SPC_F = "spc_spectrum_failing_only"
RANKING_SPC_F_P = "spc_spectrum_both"
RANKING_SPC_LAYER = "spc_spectrum_layer"
SPC_SEARCH_SPACE = "spc_search_space"
RANKING_SPECTRUM = "spectrum"
SPECTRUM_SEARCH_SPACE = "spectrum_search_space"

WORST_CASE = "worst_case"
BEST_CASE = "best_case"

def ranking(buggy_statement, mutated_project_dir, suspicious_stms_list, spectrum_expression, rank_type):
    overall_suspiciousness = {}
    for variant in suspicious_stms_list:
        variant_dir = get_variant_dir(mutated_project_dir, variant)
        statement_infor = suspiciousness_calculation(variant_dir, suspicious_stms_list[variant], spectrum_expression)
        overall_suspiciousness[variant] = statement_infor

    #Ranking with spc
    overall_results_f = ranking_failing_only(overall_suspiciousness, spectrum_expression)
    spc_ranked_list_f = spc_spectrum_ranking(overall_results_f, spectrum_expression)
    if rank_type == WORST_CASE:
        buggy_stm_spc_spectrum_ranked1 = search_rank_worst_case(buggy_statement, spc_ranked_list_f)
    else:
        buggy_stm_spc_spectrum_ranked1 = search_rank_best_case(buggy_statement, spc_ranked_list_f)

    overall_results_f_p = ranking_failing_and_passing(overall_suspiciousness, mutated_project_dir, spectrum_expression)
    spc_ranked_list_f_p = spc_spectrum_ranking(overall_results_f_p, spectrum_expression)
    if rank_type == WORST_CASE:
        buggy_stm_spc_spectrum_ranked2 = search_rank_worst_case(buggy_statement, spc_ranked_list_f_p)
    else:
        buggy_stm_spc_spectrum_ranked2 = search_rank_best_case(buggy_statement, spc_ranked_list_f_p)

    overall_results_f_p_by_layer = ranking_failing_and_passing_by_layer(overall_suspiciousness, mutated_project_dir, spectrum_expression)
    spc_spectrum_ranked_list = spc_spectrum_ranking_by_layer(overall_results_f_p_by_layer, spectrum_expression)
    if rank_type == WORST_CASE:
        buggy_stm_spc_spectrum_ranked_by_layer = search_rank_by_layer_worst_case(buggy_statement, spc_spectrum_ranked_list)
    else:
        buggy_stm_spc_spectrum_ranked_by_layer = search_rank_by_layer_best_case(buggy_statement,
                                                                                 spc_spectrum_ranked_list)

    #spectrum ranking only
    stm_info_for_spectrum, total_passed_tests, total_failed_tests = get_information_for_spectrum_ranking(mutated_project_dir)
    stm_info_for_spectrum = spectrum_calculation(stm_info_for_spectrum, total_failed_tests, total_passed_tests, spectrum_expression)
    spectrum_ranked_list = spectrum_ranking(stm_info_for_spectrum, spectrum_expression)
    if rank_type == WORST_CASE:
        buggy_stm_spectrum_ranked = search_rank_worst_case(buggy_statement, spectrum_ranked_list)
    else:
        buggy_stm_spectrum_ranked = search_rank_best_case(buggy_statement, spectrum_ranked_list)

    ranking_results = { RANKING_SPC_F: buggy_stm_spc_spectrum_ranked1,
                        RANKING_SPC_F_P: buggy_stm_spc_spectrum_ranked2,
                        RANKING_SPC_LAYER: buggy_stm_spc_spectrum_ranked_by_layer,
                        SPC_SEARCH_SPACE: len(spc_spectrum_ranked_list),
                        RANKING_SPECTRUM: buggy_stm_spectrum_ranked,
                        SPECTRUM_SEARCH_SPACE: len(spectrum_ranked_list)
                       }

    return ranking_results

def get_information_for_spectrum_ranking(mutated_project_dir):
    variants_dir = get_variants_dir(mutated_project_dir)
    variants_list = os.listdir(variants_dir)
    total_failed_tests = 0
    total_passed_tests = 0
    stm_info_for_spectrum = {}
    for variant in variants_list:
        variant_dir = get_variant_dir(mutated_project_dir, variant)
        test_coverage_dir = get_test_coverage_dir(variant_dir)

        spectrum_failed_coverage_file_dir = join_path(test_coverage_dir, SPECTRUM_FAILED_COVERAGE_FILE_NAME)
        spectrum_passed_coverage_file_dir = join_path(test_coverage_dir, SPECTRUM_PASSED_COVERAGE_FILE_NAME)

        if os.path.isfile(spectrum_failed_coverage_file_dir):
            stm_info_for_spectrum = read_coverage_info_for_spectrum(stm_info_for_spectrum,
                                                                      spectrum_failed_coverage_file_dir,
                                                                      FAILED_TEST_COUNT)

        if os.path.isfile(spectrum_passed_coverage_file_dir):
            stm_info_for_spectrum = read_coverage_info_for_spectrum(stm_info_for_spectrum,
                                                                      spectrum_passed_coverage_file_dir,
                                                                      PASSED_TEST_COUNT)

        ftests, ptests = count_tests(test_coverage_dir)
        total_failed_tests += ftests
        total_passed_tests += ptests
    return stm_info_for_spectrum, total_passed_tests, total_failed_tests


def read_coverage_info_for_spectrum(statement_infor, coverage_file, kind_of_test_count):
    try:
        tree = ET.parse(coverage_file)
        root = tree.getroot()
        project = root.find("project")

        for package in project:
            for file in package:
                for line in file:
                    id = line.get('featureClass') + "." + line.get('featureLineNum')
                    if id not in statement_infor:
                        statement_infor[id] = {}
                        statement_infor[id][FAILED_TEST_COUNT] = 0
                        statement_infor[id][PASSED_TEST_COUNT] = 0
                    statement_infor[id][kind_of_test_count] = max(int(line.get('count')),
                                                                  statement_infor[id][kind_of_test_count])
        return statement_infor
    except:
        logging.info("Exception when parsing %s", coverage_file)


def ranking_failing_only(overall_suspiciousness, spectrum_expression):
    score_type = spectrum_expression + "_score"
    overall_results = {}

    for variant in overall_suspiciousness.keys():
        for stm in overall_suspiciousness[variant]:
            if stm not in overall_results.keys():
                overall_results[stm] = {}
                overall_results[stm][SUSPICIOUS] = overall_suspiciousness[variant][stm][SUSPICIOUS]
                overall_results[stm][COUNT] = 1
                overall_results[stm][score_type] = overall_suspiciousness[variant][stm][score_type]
            else:
                if overall_results[stm][SUSPICIOUS] == False:
                    overall_results[stm][SUSPICIOUS] = overall_suspiciousness[variant][stm][SUSPICIOUS]

                overall_results[stm][COUNT] += 1
                overall_results[stm][score_type] += overall_suspiciousness[variant][stm][score_type]

    return calculate_average_supiciousness(overall_results, spectrum_expression)

def calculate_average_supiciousness(overall_results, spectrum_expression):
    score_type = spectrum_expression + "_score"
    score_average = spectrum_expression + "_average"

    for stm in overall_results:
        overall_results[stm][score_average] = overall_results[stm][score_type] / overall_results[stm][COUNT]

    return overall_results

def ranking_failing_and_passing(overall_suspiciousness, mutated_project_dir, spectrum_expression):
    passing_coverage_info = {}
    variants_dir = get_variants_dir(mutated_project_dir)
    variants_list = os.listdir(variants_dir)
    for variant in variants_list:
        if variant not in overall_suspiciousness.keys():
            read_coverage_info_for_ranking_with_passing_products(passing_coverage_info, variant, mutated_project_dir)

    overall_results2 = ranking_failing_only(overall_suspiciousness, spectrum_expression)

    for stm in overall_results2:
        for variant in passing_coverage_info:
            if stm in passing_coverage_info[variant]:
                overall_results2[stm][COUNT] += 1

    return calculate_average_supiciousness(overall_results2, spectrum_expression)

def ranking_failing_and_passing_by_layer(overall_suspiciousness, mutated_project_dir, spectrum_expression):
    passing_coverage_info = {}
    variants_dir = get_variants_dir(mutated_project_dir)
    variants_list = os.listdir(variants_dir)
    for variant in variants_list:
        if variant not in overall_suspiciousness.keys():
            read_coverage_info_for_ranking_with_passing_products(passing_coverage_info, variant, mutated_project_dir)

    overall_results2 = ranking_failing_only(overall_suspiciousness, spectrum_expression)

    for stm in overall_results2:
        overall_results2[stm][PASSING_COUNT] = 0
        for variant in passing_coverage_info:
            if stm in passing_coverage_info[variant]:
                overall_results2[stm][PASSING_COUNT] += 1

    return calculate_average_supiciousness(overall_results2, spectrum_expression)


def read_coverage_info_for_ranking_with_passing_products(passing_coverage_info, variant, mutated_project_dir):
    variant_dir = get_variant_dir(mutated_project_dir, variant)
    test_coverage_dir = get_test_coverage_dir(variant_dir)
    spectrum_passed_coverage_file_dir = join_path(test_coverage_dir, SPECTRUM_PASSED_COVERAGE_FILE_NAME)
    passing_coverage_info[variant] = []
    try:
        tree = ET.parse(spectrum_passed_coverage_file_dir)
        root = tree.getroot()
        project = root.find("project")

        for package in project:
            for file in package:
                for line in file:
                    id = line.get('featureClass') + "." + line.get('featureLineNum')
                    if id not in passing_coverage_info and int(line.get('count')) > 0:
                        passing_coverage_info[variant].append(id)

        return passing_coverage_info
    except:
        logging.info("Exception when parsing %s", spectrum_passed_coverage_file_dir)


def suspiciousness_calculation(variant_dir, suspicious_stms_list, spectrum_expression):
    statement_infor = {}
    test_coverage_dir = get_test_coverage_dir(variant_dir)

    spectrum_failed_coverage_file_dir = join_path(test_coverage_dir, SPECTRUM_FAILED_COVERAGE_FILE_NAME)
    spectrum_passed_coverage_file_dir = join_path(test_coverage_dir, SPECTRUM_PASSED_COVERAGE_FILE_NAME)

    if os.path.isfile(spectrum_failed_coverage_file_dir):
        statement_infor = read_statement_infor_from_coverage_file(statement_infor, spectrum_failed_coverage_file_dir,
                                                                  FAILED_TEST_COUNT, suspicious_stms_list)

    if os.path.isfile(spectrum_passed_coverage_file_dir):
        statement_infor = read_statement_infor_from_coverage_file(statement_infor, spectrum_passed_coverage_file_dir,
                                                                  PASSED_TEST_COUNT, suspicious_stms_list)

    (total_failed_tests, total_passed_tests) = count_tests(test_coverage_dir)

    statement_infor = spectrum_calculation(statement_infor, total_failed_tests, total_passed_tests, spectrum_expression)

    return statement_infor


def count_tests(dir):
    failed_test_dir = join_path(dir, FAILED_TEST_COVERAGE_FOLDER_NAME)
    passed_test_dir = join_path(dir, PASSED_TEST_COVERAGE_FOLDER_NAME)

    num_of_failed_tests = 0
    num_of_passed_tests = 0
    if os.path.isdir(failed_test_dir):
        num_of_failed_tests = len(os.listdir(failed_test_dir))

    if os.path.isdir(passed_test_dir):
        num_of_passed_tests = len(os.listdir(passed_test_dir))

    return num_of_failed_tests, num_of_passed_tests


def read_statement_infor_from_coverage_file(statement_infor, coverage_file, kind_of_test_count, suspicious_stms_list):
    try:
        tree = ET.parse(coverage_file)
        root = tree.getroot()
        project = root.find("project")

        for package in project:
            for file in package:
                for line in file:
                    id = line.get('featureClass') + "." + line.get('featureLineNum')
                    if id not in statement_infor:
                        statement_infor[id] = {}
                        statement_infor[id][FAILED_TEST_COUNT] = 0
                        statement_infor[id][PASSED_TEST_COUNT] = 0

                        if id in suspicious_stms_list.keys():
                            statement_infor[id][SUSPICIOUS] = True
                        else:
                            statement_infor[id][SUSPICIOUS] = False
                    statement_infor[id][kind_of_test_count] = max(int(line.get('count')),
                                                                  statement_infor[id][kind_of_test_count])
        return statement_infor
    except:
        logging.info("Exception when parsing %s", coverage_file)


def spectrum_calculation(statement_infor, total_failed_tests, total_passed_tests, spectrum_expression):
    for id in statement_infor.keys():
        if spectrum_expression == TARANTULA:
            statement_infor[id][TARANTULA_SCORE] = tarantula_calculation(statement_infor[id][FAILED_TEST_COUNT], statement_infor[id][PASSED_TEST_COUNT], total_failed_tests,
                                                                         total_passed_tests)
        elif spectrum_expression == OCHIAI:
            statement_infor[id][OCHIAI_SCORE] = ochiai_calculation(statement_infor[id][FAILED_TEST_COUNT], statement_infor[id][PASSED_TEST_COUNT],
                                                                   total_failed_tests)
        elif spectrum_expression == OP2:
            statement_infor[id][OP2_SCORE] = op2_calculation(statement_infor[id][FAILED_TEST_COUNT], statement_infor[id][PASSED_TEST_COUNT],
                                                             total_passed_tests)
        elif spectrum_expression == BARINEL:
            statement_infor[id][BARINEL_SCORE] = barinel_calculation(statement_infor[id][FAILED_TEST_COUNT], statement_infor[id][PASSED_TEST_COUNT])
        elif spectrum_expression == DSTAR:
            statement_infor[id][DSTAR_SCORE] = dstar_calculation(statement_infor[id][FAILED_TEST_COUNT], statement_infor[id][PASSED_TEST_COUNT], total_failed_tests)
    return statement_infor


def spectrum_ranking(statements_infor, spectrum_expression):
    spectrum_ranked_list = []

    score_type = spectrum_expression + "_score"
    for (key, value) in statements_infor.items():
        spectrum_ranked_list.append((key, statements_infor[key][score_type]))

    for i in range(0, len(spectrum_ranked_list) - 1):
        for j in range(i + 1, len(spectrum_ranked_list)):
            if spectrum_ranked_list[i][1] < spectrum_ranked_list[j][1]:
                spectrum_ranked_list[i], spectrum_ranked_list[j] = \
                    spectrum_ranked_list[j], spectrum_ranked_list[i]

    return spectrum_ranked_list


def spc_spectrum_ranking(statements_infor, spectrum_expression):
    spc_spectrum_ranked_list = []
    score_type = spectrum_expression + "_average"

    for (key, value) in statements_infor.items():
        if statements_infor[key][SUSPICIOUS]:
            spc_spectrum_ranked_list.append((key, statements_infor[key][score_type]))

    for i in range(0, len(spc_spectrum_ranked_list) - 1):
        for j in range(i + 1, len(spc_spectrum_ranked_list)):
            if spc_spectrum_ranked_list[i][1] < spc_spectrum_ranked_list[j][1]:
                spc_spectrum_ranked_list[i], spc_spectrum_ranked_list[j] = \
                    spc_spectrum_ranked_list[j], spc_spectrum_ranked_list[i]

    return spc_spectrum_ranked_list

def spc_spectrum_ranking_by_layer(statements_infor, spectrum_expression):
    spc_spectrum_ranked_list = []
    score_type = spectrum_expression + "_average"

    for (key, value) in statements_infor.items():
        if statements_infor[key][SUSPICIOUS]:
            spc_spectrum_ranked_list.append((key, statements_infor[key][score_type], statements_infor[key][PASSING_COUNT]))

    for i in range(0, len(spc_spectrum_ranked_list) - 1):
        for j in range(i + 1, len(spc_spectrum_ranked_list)):
            if spc_spectrum_ranked_list[i][1] < spc_spectrum_ranked_list[j][1]:
                spc_spectrum_ranked_list[i], spc_spectrum_ranked_list[j] = \
                    spc_spectrum_ranked_list[j], spc_spectrum_ranked_list[i]
            elif spc_spectrum_ranked_list[i][1] == spc_spectrum_ranked_list[j][1]:
                if spc_spectrum_ranked_list[i][2] > spc_spectrum_ranked_list[j][2]:
                    spc_spectrum_ranked_list[i], spc_spectrum_ranked_list[j] = \
                        spc_spectrum_ranked_list[j], spc_spectrum_ranked_list[i]
    return spc_spectrum_ranked_list

def search_rank_worst_case(stm, ranked_list):
    for i in range(0, len(ranked_list)):
        if ranked_list[i][0] == stm:
            j = i
            while( j < len(ranked_list) - 1):
               if ranked_list[j][1] == ranked_list[j + 1][1]:
                   j += 1
               else:
                   break
            return j + 1
    return -1

def search_rank_best_case(stm, ranked_list):
    for i in range(0, len(ranked_list)):
        if ranked_list[i][0] == stm:
            j = i
            while( j > 0):
               if ranked_list[j][1] == ranked_list[j - 1][1]:
                   j -= 1
               else:
                   break
            return j + 1
    return -1

def search_rank_by_layer_worst_case(stm, ranked_list):
    for i in range(0, len(ranked_list)):
        if ranked_list[i][0] == stm:
            j = i
            while( j < len(ranked_list) - 1):
               if ranked_list[j][1] == ranked_list[j + 1][1] and ranked_list[j][2] == ranked_list[j + 1][2]:
                   j += 1
               else:
                   break
            return j + 1
    return -1

def search_rank_by_layer_best_case(stm, ranked_list):
    for i in range(0, len(ranked_list)):
        if ranked_list[i][0] == stm:
            j = i
            while( j > 0):
               if ranked_list[j][1] == ranked_list[j - 1][1] and ranked_list[j][2] == ranked_list[j - 1][2]:
                   j -= 1
               else:
                   break
            return j + 1
    return -1
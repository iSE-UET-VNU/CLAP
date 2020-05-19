import logging
import os
import xml.etree.ElementTree as ET
from FileManager import join_path, SPECTRUM_FAILED_COVERAGE_FILE_NAME, SPECTRUM_PASSED_COVERAGE_FILE_NAME, \
    get_test_coverage_dir, PASSED_TEST_COVERAGE_FOLDER_NAME, FAILED_TEST_COVERAGE_FOLDER_NAME, get_variant_dir

# keywords
STM_FAILED_TEST_COUNT = 'failed_test_count'
STM_PASSED_TEST_COUNT = 'passed_test_count'
STM_SUSPICIOUS = 'suspicious'
STM_SPECTRUM_SCORE = 'spectrum_score'
STM_NUM_INTERACTIONS = 'num_interactions'

RANKING_SPECTRUM = "spectrum"
RANKING_SPECTRUM_DETAIL = "spectrum_detail"
RANKING_SPC_SPECTRUM = "spc_spectrum"
RANKING_SPC_SPECTRUM_DETAIL = "spc_spectrum_detail"
RANKING_SPC_SPECTRUM_INTERACTION = "spc_spectrum_interaction"
RANKING_SPC_SPECTRUM_INTERACTION_DETAIL = "spc_spectrum_interaction_detail"

def ranking( buggy_statement, mutated_project_dir, suspicious_stms_list):
    ranking_results = {}
    for variant in suspicious_stms_list:
        variant_dir = get_variant_dir(mutated_project_dir, variant)
        statement_infor = suspiciousness_calculation(variant_dir, suspicious_stms_list[variant])

        spectrum_ranked_list = spectrum_ranking(statement_infor)
        buggy_stm_spectrum_ranked = search_rank(buggy_statement, spectrum_ranked_list)

        spc_spectrum_ranked_list = spc_spectrum_ranking(statement_infor)
        buggy_stm_spc_spectrum_ranked = search_rank(buggy_statement, spc_spectrum_ranked_list)

        spc_interaction_spectrum_ranked_list = spc_interaction_spectrum_raking(statement_infor)
        buggy_stm_spc_interaction_spectrum_ranked = search_rank(buggy_statement, spc_interaction_spectrum_ranked_list)

        ranking_results[variant] = {RANKING_SPECTRUM: buggy_stm_spectrum_ranked,
                                    RANKING_SPECTRUM_DETAIL: spectrum_ranked_list,
                                    RANKING_SPC_SPECTRUM: buggy_stm_spc_spectrum_ranked,
                                    RANKING_SPC_SPECTRUM_DETAIL: spc_spectrum_ranked_list,
                                    RANKING_SPC_SPECTRUM_INTERACTION: buggy_stm_spc_interaction_spectrum_ranked,
                                    RANKING_SPC_SPECTRUM_INTERACTION_DETAIL: spc_interaction_spectrum_ranked_list}

    return ranking_results

def suspiciousness_calculation(variant_dir, suspicious_stms_list):
    statement_infor = {}
    test_coverage_dir = get_test_coverage_dir(variant_dir)

    spectrum_failed_coverage_file_dir = join_path(test_coverage_dir, SPECTRUM_FAILED_COVERAGE_FILE_NAME)
    spectrum_passed_coverage_file_dir = join_path(test_coverage_dir, SPECTRUM_PASSED_COVERAGE_FILE_NAME)

    if os.path.isfile(spectrum_failed_coverage_file_dir):
        statement_infor = read_statement_infor_from_coverage_file(statement_infor, spectrum_failed_coverage_file_dir,
                                                                  STM_FAILED_TEST_COUNT, suspicious_stms_list)

    if os.path.isfile(spectrum_passed_coverage_file_dir):
        statement_infor = read_statement_infor_from_coverage_file(statement_infor, spectrum_passed_coverage_file_dir,
                                                                  STM_PASSED_TEST_COUNT, suspicious_stms_list)

    (total_failed_tests, total_passed_tests) = count_tests(test_coverage_dir)

    spectrum_calculation(statement_infor, total_failed_tests, total_passed_tests)
    return statement_infor


def count_tests(dir):
    failed_test_dir = join_path(dir, FAILED_TEST_COVERAGE_FOLDER_NAME)
    passed_test_dir = join_path(dir, PASSED_TEST_COVERAGE_FOLDER_NAME)

    num_of_failed_tests = 0
    num_of_passed_tests = 0
    if (os.path.isdir(failed_test_dir)):
        num_of_failed_tests = len(os.listdir(failed_test_dir))

    if (os.path.isdir(passed_test_dir)):
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
                        statement_infor[id][STM_FAILED_TEST_COUNT] = 0
                        statement_infor[id][STM_PASSED_TEST_COUNT] = 0

                        if id in suspicious_stms_list.keys():
                            statement_infor[id][STM_SUSPICIOUS] = True
                            statement_infor[id][STM_NUM_INTERACTIONS] = suspicious_stms_list[id]['num_interactions']
                        else:
                            statement_infor[id][STM_SUSPICIOUS] = False
                            statement_infor[id][STM_NUM_INTERACTIONS] = 0

                    statement_infor[id][kind_of_test_count] = max(int(line.get('count')),
                                                                  statement_infor[id][kind_of_test_count])
        return statement_infor
    except:
        logging.info("Exception when parsing %s", coverage_file)


def spectrum_calculation(statement_infor, total_failed_tests, total_passed_tests):
    for id in statement_infor.keys():
        statement_infor[id][STM_SPECTRUM_SCORE] = stm_spectrum_calculation(statement_infor, id, total_failed_tests,
                                                                       total_passed_tests)
    return statement_infor


def stm_spectrum_calculation(statement_infor, stm_id, total_failed_tests, total_passed_tests):
    if (total_failed_tests == 0 or total_passed_tests == 0):
        return -1

    if (statement_infor[stm_id][STM_FAILED_TEST_COUNT] == 0 and statement_infor[stm_id][STM_PASSED_TEST_COUNT] == 0):
        return -1

    return (statement_infor[stm_id][STM_FAILED_TEST_COUNT] / total_failed_tests) / \
           ((statement_infor[stm_id][STM_FAILED_TEST_COUNT] / total_failed_tests) +
            (statement_infor[stm_id][STM_PASSED_TEST_COUNT] / total_passed_tests))


def spectrum_ranking(statement_infor):
    spectrum_ranked_list = []
    for (key, value) in statement_infor.items():
        spectrum_ranked_list.append((key, statement_infor[key][STM_SPECTRUM_SCORE]))

    for i in range(0, len(spectrum_ranked_list) - 1):
        for j in range(i + 1, len(spectrum_ranked_list)):
            if spectrum_ranked_list[i][1] < spectrum_ranked_list[j][1]:
                spectrum_ranked_list[i], spectrum_ranked_list[j] = \
                    spectrum_ranked_list[j], spectrum_ranked_list[i]

    return spectrum_ranked_list


def spc_spectrum_ranking(statement_infor):
    spc_spectrum_ranked_list = []

    for (key, value) in statement_infor.items():
        if statement_infor[key][STM_SUSPICIOUS] == True:
            spc_spectrum_ranked_list.append((key, statement_infor[key][STM_SPECTRUM_SCORE]))

    for i in range(0, len(spc_spectrum_ranked_list) - 1):
        for j in range(i + 1, len(spc_spectrum_ranked_list)):
            if spc_spectrum_ranked_list[i][1] < spc_spectrum_ranked_list[j][1]:
                spc_spectrum_ranked_list[i], spc_spectrum_ranked_list[j] = \
                    spc_spectrum_ranked_list[j], spc_spectrum_ranked_list[i]

    return spc_spectrum_ranked_list


def spc_interaction_spectrum_raking(statement_infor):
    spc_interaction_spectrum_ranked_list = []
    for (key, value) in statement_infor.items():
        if statement_infor[key][STM_SUSPICIOUS] == True:
            spc_interaction_spectrum_ranked_list.append(
                (key, statement_infor[key][STM_SPECTRUM_SCORE], statement_infor[key][STM_NUM_INTERACTIONS]))

    for i in range(0, len(spc_interaction_spectrum_ranked_list) - 1):
        for j in range(i + 1, len(spc_interaction_spectrum_ranked_list)):
            if spc_interaction_spectrum_ranked_list[i][1] < spc_interaction_spectrum_ranked_list[j][1]:

                spc_interaction_spectrum_ranked_list[i], spc_interaction_spectrum_ranked_list[j] = \
                    spc_interaction_spectrum_ranked_list[j], spc_interaction_spectrum_ranked_list[i]

            elif (spc_interaction_spectrum_ranked_list[i][1] == spc_interaction_spectrum_ranked_list[j][1] and
                  spc_interaction_spectrum_ranked_list[i][2] < spc_interaction_spectrum_ranked_list[j][2]):

                spc_interaction_spectrum_ranked_list[i], spc_interaction_spectrum_ranked_list[j] = \
                    spc_interaction_spectrum_ranked_list[j], spc_interaction_spectrum_ranked_list[i]
    return spc_interaction_spectrum_ranked_list


def search_rank(stm, ranked_list):
    for item in ranked_list:
        if item[0] == stm:
            return ranked_list.index(item) + 1

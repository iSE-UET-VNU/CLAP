import os
import xml.etree.ElementTree as ET

from FileManager import join_path, SPECTRUM_FAILED_COVERAGE_FILE_NAME, SPECTRUM_PASSED_COVERAGE_FILE_NAME

statement_infor = {}
#key is package_file_linenum of statement in the variant
#value contains:
FAILED_TEST_COUNT = 'failed_test_count'
PASSED_TEST_COUNT = 'passed_test_count'
FEATURE_CLASS = 'featureClass'
FEATURE_LINE_NUM = 'featureLineNum'
SUSPICIOUS = 'suspicious'
SPECTRUM_SCORE = 'spectrum_score'
NUM_INTERACTIONS = 'num_interactions'


def suspiciousness_calculation(dir, suspicious_stms_list):
    spectrum_failed_coverage_file_dir = join_path(dir, SPECTRUM_FAILED_COVERAGE_FILE_NAME)
    spectrum_passed_coverage_file_dir = join_path(dir, SPECTRUM_PASSED_COVERAGE_FILE_NAME)

    update_statement_infor(spectrum_failed_coverage_file_dir, FAILED_TEST_COUNT, suspicious_stms_list)
    update_statement_infor(spectrum_passed_coverage_file_dir, PASSED_TEST_COUNT, suspicious_stms_list)

    (total_failed_tests, total_passed_tests) = count_tests(dir)

    spectrum_calculation(total_failed_tests, total_passed_tests)


def count_tests(dir):
    failed_test_dir = join_path(dir, "failed")
    passed_test_dir = join_path(dir, "passed")
    total_failed_tests = len(os.listdir(failed_test_dir))
    total_passed_tests = len(os.listdir(passed_test_dir))

    return total_failed_tests, total_passed_tests


def update_statement_infor(coverage_file, kind_of_test_count, suspicious_stms_list):
    tree = ET.parse(coverage_file)
    root = tree.getroot()
    project = root.find("project")

    for package in project:
        for file in package:
            for line in file:
                id = file.get('name') + "." + line.get('num')
                if id in statement_infor:
                    if(kind_of_test_count in statement_infor[id]):
                        statement_infor[id][kind_of_test_count] = max(int(line.get('count')),  statement_infor[id][kind_of_test_count])
                    else:
                        statement_infor[id][kind_of_test_count] = int(line.get('count'))
                else:
                    statement_infor[id] = {}
                    statement_infor[id][FEATURE_CLASS] = line.get('featureClass')
                    statement_infor[id][FEATURE_LINE_NUM] = line.get('featureLineNum')
                    if id in suspicious_stms_list.keys():
                        statement_infor[id][SUSPICIOUS] = True
                        statement_infor[id][NUM_INTERACTIONS] = suspicious_stms_list[id]['num_interactions']
                    else:
                        statement_infor[id][SUSPICIOUS] = False

                    statement_infor[id][kind_of_test_count] = int(line.get('count'))


def spectrum_calculation(total_failed_tests, total_passed_tests):
   for id in statement_infor:
        statement_infor[id][SPECTRUM_SCORE] = stm_spectrum_calculation(id, total_failed_tests, total_passed_tests)

def stm_spectrum_calculation(stm_id, total_failed_tests, total_passed_tests):
    if(statement_infor[stm_id][FAILED_TEST_COUNT] == 0 and statement_infor[stm_id][PASSED_TEST_COUNT] == 0):
        return -1
    return (statement_infor[stm_id][FAILED_TEST_COUNT]/ total_failed_tests) / \
           ((statement_infor[stm_id][FAILED_TEST_COUNT]/ total_failed_tests) +
            (statement_infor[stm_id][PASSED_TEST_COUNT]/total_passed_tests))

def spectrum_ranking():
    spectrum_ranked_list = []
    for (key, value) in statement_infor.items():
            spectrum_ranked_list.append((statement_infor[key][FEATURE_CLASS] + "." +
                                                         statement_infor[key][FEATURE_LINE_NUM],
                                                         statement_infor[key][SPECTRUM_SCORE]))

    for i in range(0, len(spectrum_ranked_list) - 1):
        for j in range(i + 1, len(spectrum_ranked_list)):
            if spectrum_ranked_list[i][1] < spectrum_ranked_list[j][1]:
                spectrum_ranked_list[i], spectrum_ranked_list[j] = \
                spectrum_ranked_list[j], spectrum_ranked_list[i]

    return spectrum_ranked_list

def spc_spectrum_ranking():
    spc_spectrum_ranked_list = []

    for (key, value) in statement_infor.items():
        if statement_infor[key][SUSPICIOUS] == True:
            spc_spectrum_ranked_list.append((statement_infor[key][FEATURE_CLASS] + "." +
                                                         statement_infor[key][FEATURE_LINE_NUM],
                                                         statement_infor[key][SPECTRUM_SCORE]))

    for i in range(0, len(spc_spectrum_ranked_list) - 1):
        for j in range(i + 1, len(spc_spectrum_ranked_list)):
            if spc_spectrum_ranked_list[i][1] < spc_spectrum_ranked_list[j][1]:
                spc_spectrum_ranked_list[i], spc_spectrum_ranked_list[j] = \
                spc_spectrum_ranked_list[j], spc_spectrum_ranked_list[i]

    return spc_spectrum_ranked_list

def spc_interaction_spectrum_raking():
    spc_interaction_spectrum_ranked_list = []
    for (key, value) in statement_infor.items():
        if statement_infor[key][SUSPICIOUS] == True:
            spc_interaction_spectrum_ranked_list.append((statement_infor[key][FEATURE_CLASS] + "." + statement_infor[key][FEATURE_LINE_NUM],
                                                         statement_infor[key][SPECTRUM_SCORE], statement_infor[key][NUM_INTERACTIONS]))

    for i in range(0, len(spc_interaction_spectrum_ranked_list) - 1):
        for j in range(i + 1, len(spc_interaction_spectrum_ranked_list)):
            if spc_interaction_spectrum_ranked_list[i][1] <  spc_interaction_spectrum_ranked_list[j][1]:

                spc_interaction_spectrum_ranked_list[i], spc_interaction_spectrum_ranked_list[j] = \
                    spc_interaction_spectrum_ranked_list[j], spc_interaction_spectrum_ranked_list[i]

            elif(spc_interaction_spectrum_ranked_list[i][1] ==  spc_interaction_spectrum_ranked_list[j][1] and
                 spc_interaction_spectrum_ranked_list[i][2] <  spc_interaction_spectrum_ranked_list[j][2]):

                spc_interaction_spectrum_ranked_list[i], spc_interaction_spectrum_ranked_list[j] = \
                spc_interaction_spectrum_ranked_list[j], spc_interaction_spectrum_ranked_list[i]
    return spc_interaction_spectrum_ranked_list

def search_rank(stm, ranked_list):
    for item in ranked_list:
        if item[0] == stm:
            return ranked_list.index(item) + 1


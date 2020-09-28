import logging
import os
import xml.etree.ElementTree as ET

from FileManager import join_path, SPECTRUM_FAILED_COVERAGE_FILE_NAME, SPECTRUM_PASSED_COVERAGE_FILE_NAME, \
    get_test_coverage_dir, PASSED_TEST_COVERAGE_FOLDER_NAME, FAILED_TEST_COVERAGE_FOLDER_NAME, get_variant_dir, \
    get_variants_dir

# keywords
from Spectrum_Expression import tarantula_calculation, ochiai_calculation, op2_calculation, barinel_calculation, \
    dstar_calculation, TARANTULA_SCORE, TARANTULA, OCHIAI, OCHIAI_SCORE, OP2_SCORE, OP2, BARINEL, BARINEL_SCORE, DSTAR, \
    DSTAR_SCORE, RUSSELL_RAO, RUSSELL_RAO_SCORE, \
    russell_rao_calculation, SIMPLE_MATCHING, simple_matching_calculation, ROGERS_TANIMOTO, SIMPLE_MATCHING_SCORE, \
    ROGERS_TANIMOTO_SCORE, rogers_tanimoto_calculation, AMPLE_SCORE, AMPLE, ample_calculation, JACCARD, JACCARD_SCORE, \
    jaccard_calculation, COHEN, COHEN_SCORE, cohen_calculation, SCOTT_SCORE, SCOTT, \
    scott_calculation, ROGOT1_SCORE, ROGOT1, rogot1_calculation, GEOMETRIC_MEAN_SCORE, GEOMETRIC_MEAN, \
    geometric_mean_calculation, M2, M2_SCORE, \
    m2_calculation, WONG1, wong1_calculation, WONG1_SCORE, SOKAL_SCORE, SOKAL, sokal_calculation

FAILED_TEST_COUNT = 'failed_test_count'
PASSED_TEST_COUNT = 'passed_test_count'
SUSPICIOUS = 'suspicious'
COUNT = "count"
PASSING_COUNT = "passing_count"

VARCOP_SPC_FAILING = "spc_spectrum_failing_only"
VARCOP_SPC_LAYER = "spc_spectrum_layer"
VARCOP_SPC_SEARCH_SPACE = "spc_search_space"
SPECTRUM = "spectrum"
SPECTRUM_SEARCH_SPACE = "spectrum_search_space"

VARCOP_FAILING = "WITHOUT_ISOLATION_F"
VARCOP_LAYER = "WITHOUT_ISOLATION_LAYER"
VARCOP_SEARCH_SPACE = "WITHOUT_ISOLATION_SPACE"

def suspicious_stms_of_the_system(suspicious_stms_list):
    stm_set = []
    for variant in suspicious_stms_list:
        for stm in suspicious_stms_list[variant]:
            if stm not in stm_set:
                stm_set.append(stm)
    return len(stm_set)

def rank_for_a_suspicious_list(mutated_project_dir, buggy_statement, all_stms_of_the_system, suspicious_stms_list, spectrum_expression):
    num_suspicious_stm = suspicious_stms_of_the_system(suspicious_stms_list)
    overall_suspiciousness = {}
    for variant in suspicious_stms_list:
        variant_dir = get_variant_dir(mutated_project_dir, variant)
        statement_infor = suspiciousness_calculation(variant_dir, suspicious_stms_list[variant], spectrum_expression)
        overall_suspiciousness[variant] = spc_spectrum_ranking(statement_infor, spectrum_expression)

    ranked_list = overall_suspiciousness_score(all_stms_of_the_system, suspicious_stms_list,
                                                     overall_suspiciousness, spectrum_expression)

    buggy_stm_ranked = search_buggy_stms(buggy_statement, ranked_list)
    buggy_stm_ranked_by_layer = search_buggy_stms_by_layer(buggy_statement, ranked_list)
    return buggy_stm_ranked, buggy_stm_ranked_by_layer, num_suspicious_stm

def get_all_stms_in_failing_products(all_stms_of_the_system, failing_variants):
    suspicious_stms_list = {}
    for variant in failing_variants:
        suspicious_stms_list[variant] = all_stms_of_the_system[variant]
    return suspicious_stms_list


def ranking(buggy_statement, mutated_project_dir, suspicious_stms_list, spectrum_expression):

    all_stms_of_the_system = get_all_stms_of_the_system(mutated_project_dir)


    #rank with isolation
    buggy_stm_ranked, buggy_stm_ranked_by_layer, num_suspicious_stm = rank_for_a_suspicious_list(mutated_project_dir, buggy_statement, all_stms_of_the_system, suspicious_stms_list,
                        spectrum_expression)

    all_suspicious_of_the_system = get_all_stms_in_failing_products(all_stms_of_the_system, suspicious_stms_list.keys())

    #rank without isolation
    buggy_stm_ranked2, buggy_stm_ranked_by_layer2, num_suspicious_stm2 = rank_for_a_suspicious_list(mutated_project_dir, buggy_statement, all_stms_of_the_system, all_suspicious_of_the_system,
        spectrum_expression)

    #spectrum ranking only
    buggy_stm_spectrum_ranked, spectrum_space = rank_by_tranditional_spectrum(mutated_project_dir, spectrum_expression, buggy_statement)

    ranking_results = { VARCOP_SPC_FAILING: buggy_stm_ranked,
                        VARCOP_SPC_LAYER: buggy_stm_ranked_by_layer,
                        VARCOP_SPC_SEARCH_SPACE: num_suspicious_stm,
                        VARCOP_FAILING: buggy_stm_ranked2,
                        VARCOP_LAYER: buggy_stm_ranked_by_layer2,
                        VARCOP_SEARCH_SPACE: num_suspicious_stm2,
                        SPECTRUM: buggy_stm_spectrum_ranked,
                        SPECTRUM_SEARCH_SPACE: spectrum_space
                       }

    return ranking_results

def get_stms_from_list_varints(stms_in_list_variants):
    all_stms_list = []
    for variant in stms_in_list_variants:
        for stm in stms_in_list_variants[variant]:
            if stm not in all_stms_list:
                all_stms_list.append(stm)
    return all_stms_list

def overall_suspiciousness_score(all_stms_of_the_system, suspicious_stms_list, overall_suspiciousness, spectrum_expression):
    score_type = spectrum_expression + "_score"
    all_stms_list = get_stms_from_list_varints(suspicious_stms_list)
    all_stms_score_list = {}

    for variant in overall_suspiciousness:
        for stm in all_stms_list:
            #if the stm appears in the suspicious stms list of the product [variant]
            if stm in suspicious_stms_list[variant]:
                rank = search_rank_worst_case(stm, overall_suspiciousness[variant])
                #if stms is suspicious then its score is the rank of the stm in the suspicious set
                if(rank != -1):
                    if stm in all_stms_score_list:
                        all_stms_score_list[stm][score_type] += rank
                    if stm not in all_stms_score_list:
                        all_stms_score_list[stm] = {}
                        all_stms_score_list[stm][score_type] = rank
                # if stms is not suspicious then its score is the size of the product
                else:
                    if stm in all_stms_score_list:
                        all_stms_score_list[stm][score_type] += len(suspicious_stms_list[variant])
                    if stm not in all_stms_score_list:
                        all_stms_score_list[stm] = {}
                        all_stms_score_list[stm][score_type] = len(suspicious_stms_list[variant])
            #if the stm does not appear int the product [variant]
            #then its score is the size of the system's stms list
            else:
                if stm in all_stms_score_list:
                    all_stms_score_list[stm][score_type] += len(all_stms_list)
                if stm not in all_stms_score_list:
                    all_stms_score_list[stm] = {}
                    all_stms_score_list[stm][score_type] = len(all_stms_list)

    for stm in all_stms_score_list:
        all_stms_score_list[stm]["num_passing_product"] = 0
        for variant in all_stms_of_the_system:
            if variant not in suspicious_stms_list.keys() and stm in all_stms_of_the_system[variant]:
                all_stms_score_list[stm]["num_passing_product"] += 1

    return varcop_ranking(all_stms_score_list, spectrum_expression)


def rank_by_tranditional_spectrum(mutated_project_dir, spectrum_expression, buggy_statement):
    stm_info_for_spectrum, total_passed_tests, total_failed_tests = get_information_for_spectrum_ranking(
        mutated_project_dir)
    stm_info_for_spectrum = spectrum_calculation(stm_info_for_spectrum, total_failed_tests, total_passed_tests,
                                                 spectrum_expression)
    spectrum_ranked_list = spectrum_ranking(stm_info_for_spectrum, spectrum_expression)

    buggy_stm_spectrum_ranked = search_rank_worst_case(buggy_statement, spectrum_ranked_list)
    space = len(spectrum_ranked_list)
    return buggy_stm_spectrum_ranked, space

def get_all_stms_of_the_system(mutated_project_dir):
    variants_dir = get_variants_dir(mutated_project_dir)
    variants_list = os.listdir(variants_dir)
    stm_list = {}
    for variant in variants_list:
        variant_dir = get_variant_dir(mutated_project_dir, variant)
        test_coverage_dir = get_test_coverage_dir(variant_dir)
        coverage_files = []
        coverage_files.append(join_path(test_coverage_dir, SPECTRUM_FAILED_COVERAGE_FILE_NAME))
        coverage_files.append(join_path(test_coverage_dir, SPECTRUM_PASSED_COVERAGE_FILE_NAME))

        for file in coverage_files:
            if os.path.isfile(file):
                data = {}
                try:
                    tree = ET.parse(file)
                    root = tree.getroot()
                    project = root.find("project")

                    for package in project:
                        for file in package:
                            for line in file:
                                id = line.get('featureClass') + "." + line.get('featureLineNum')
                                if id not in data:
                                    data[id] = {'num_interactions': 0}
                except:
                    logging.info("Exception when parsing %s", file)
                stm_list[variant] = data
    return stm_list

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
    data = {}
    try:
        tree = ET.parse(coverage_file)
        root = tree.getroot()
        project = root.find("project")

        for package in project:
            for file in package:
                for line in file:
                    id = line.get('featureClass') + "." + line.get('featureLineNum')
                    if id not in data:
                        data[id] = {}
                        data[id][FAILED_TEST_COUNT] = 0
                        data[id][PASSED_TEST_COUNT] = 0
                    data[id][kind_of_test_count] = max(int(line.get('count')),
                                                                  data[id][kind_of_test_count])

        for id in data.keys():
            if id not in statement_infor:
                statement_infor[id] = data[id]
            else:
                statement_infor[id][kind_of_test_count] += data[id][kind_of_test_count]
        return statement_infor
    except:
        logging.info("Exception when parsing %s", coverage_file)


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
            statement_infor[id][DSTAR_SCORE] = dstar_calculation(statement_infor[id][FAILED_TEST_COUNT],
                                                                          statement_infor[id][PASSED_TEST_COUNT],
                                                                          total_failed_tests)
        elif spectrum_expression == RUSSELL_RAO:
            statement_infor[id][RUSSELL_RAO_SCORE] = russell_rao_calculation(statement_infor[id][FAILED_TEST_COUNT],
                                                                 total_failed_tests, total_passed_tests)
        elif spectrum_expression == SIMPLE_MATCHING:
            statement_infor[id][SIMPLE_MATCHING_SCORE] = simple_matching_calculation(statement_infor[id][FAILED_TEST_COUNT], statement_infor[id][PASSED_TEST_COUNT],
                                                                 total_failed_tests, total_passed_tests)
        elif spectrum_expression == ROGERS_TANIMOTO:
            statement_infor[id][ROGERS_TANIMOTO_SCORE] = rogers_tanimoto_calculation(statement_infor[id][FAILED_TEST_COUNT], statement_infor[id][PASSED_TEST_COUNT],
                                                                 total_failed_tests, total_passed_tests)
        elif spectrum_expression == AMPLE:
            statement_infor[id][AMPLE_SCORE] = ample_calculation(statement_infor[id][FAILED_TEST_COUNT], statement_infor[id][PASSED_TEST_COUNT],
                                                                 total_failed_tests, total_passed_tests)
        elif spectrum_expression == JACCARD:
            statement_infor[id][JACCARD_SCORE] = jaccard_calculation(statement_infor[id][FAILED_TEST_COUNT],
                                                                 statement_infor[id][PASSED_TEST_COUNT],
                                                                 total_failed_tests)
        elif spectrum_expression == COHEN:
            statement_infor[id][COHEN_SCORE] = cohen_calculation(statement_infor[id][FAILED_TEST_COUNT], statement_infor[id][PASSED_TEST_COUNT],
                                                                 total_failed_tests, total_passed_tests)

        elif spectrum_expression == SCOTT:
            statement_infor[id][SCOTT_SCORE] = scott_calculation(statement_infor[id][FAILED_TEST_COUNT],
                                                                 statement_infor[id][PASSED_TEST_COUNT],
                                                                 total_failed_tests, total_passed_tests)
        elif spectrum_expression == ROGOT1:
            statement_infor[id][ROGOT1_SCORE] = rogot1_calculation(statement_infor[id][FAILED_TEST_COUNT],
                                                                 statement_infor[id][PASSED_TEST_COUNT],
                                                                 total_failed_tests, total_passed_tests)
        elif spectrum_expression == GEOMETRIC_MEAN:

            statement_infor[id][GEOMETRIC_MEAN_SCORE] = geometric_mean_calculation(statement_infor[id][FAILED_TEST_COUNT],
                                                                     statement_infor[id][PASSED_TEST_COUNT],
                                                                     total_failed_tests, total_passed_tests)

        elif spectrum_expression == M2:
            statement_infor[id][M2_SCORE] = m2_calculation(statement_infor[id][FAILED_TEST_COUNT],
                                                                          statement_infor[id][PASSED_TEST_COUNT],
                                                                          total_failed_tests, total_passed_tests)
        elif spectrum_expression == WONG1:
            statement_infor[id][WONG1_SCORE] = wong1_calculation(statement_infor[id][FAILED_TEST_COUNT])

        elif spectrum_expression == SOKAL:
            statement_infor[id][SOKAL_SCORE] = sokal_calculation(statement_infor[id][FAILED_TEST_COUNT],
                                                                     statement_infor[id][PASSED_TEST_COUNT],
                                                                     total_failed_tests, total_passed_tests)
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


def varcop_ranking(statements_infor, spectrum_expression):
    ranked_list = []

    score_type = spectrum_expression + "_score"
    for (key, value) in statements_infor.items():
        ranked_list.append((key, statements_infor[key][score_type], statements_infor[key]["num_passing_product"]))

    for i in range(0, len(ranked_list) - 1):
        for j in range(i + 1, len(ranked_list)):
            if ranked_list[i][1] < ranked_list[j][1]:
                ranked_list[i], ranked_list[j] = \
                    ranked_list[j], ranked_list[i]

    return ranked_list


def spc_spectrum_ranking(statements_infor, spectrum_expression):
    spc_spectrum_ranked_list = []
    score_type = spectrum_expression + "_score"

    for (key, value) in statements_infor.items():
        if statements_infor[key][SUSPICIOUS]:
            spc_spectrum_ranked_list.append((key, statements_infor[key][score_type]))

    for i in range(0, len(spc_spectrum_ranked_list) - 1):
        for j in range(i + 1, len(spc_spectrum_ranked_list)):
            if spc_spectrum_ranked_list[i][1] < spc_spectrum_ranked_list[j][1]:
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


def search_buggy_stms(stm, ranked_list):
    for i in range(len(ranked_list)- 1, 0, -1):
        if ranked_list[i][0] == stm:
            j = i;
            while( j >= 0):
                if ranked_list[j][1] == ranked_list[j-1][1]:
                    j -= 1
                else:
                    break;
            return len(ranked_list) - j
    return -1

def search_buggy_stms_by_layer(stm, ranked_list):
    for i in range(len(ranked_list)- 1, 0, -1):
        if ranked_list[i][0] == stm:
            j = i;
            while( j >= 0):
                if ranked_list[j][1] == ranked_list[j-1][1] and ranked_list[j][2] == ranked_list[j-1][2]:
                    j -= 1
                else:
                    break;
            return len(ranked_list) - j
    return -1
import logging
import os

import xml.etree.ElementTree as ET

from FileManager import get_variant_dir, get_test_coverage_dir, join_path, \
    SPECTRUM_FAILED_COVERAGE_FILE_NAME, SPECTRUM_PASSED_COVERAGE_FILE_NAME

from Spectrum_Expression import tarantula_calculation, ochiai_calculation, op2_calculation, barinel_calculation, \
    dstar_calculation, TARANTULA_SCORE, TARANTULA, OCHIAI, OCHIAI_SCORE, OP2, OP2_SCORE, BARINEL, BARINEL_SCORE, DSTAR, \
    DSTAR_SCORE

from TestingCoverageManager import statement_coverage_of_variants

STATEMENT_ID = "stm_id"
VARIANTS_FAILED = "variants_failed"
VARIANTS_PASSED = "variants_passed"

def features_ranking(buggy_statement, mutated_project_dir, failling_variants, filter_coverage_rate, ranking_type):
    total_variants = 0
    variants_testing_coverage = statement_coverage_of_variants(mutated_project_dir)
    features_info = {}
    for variant in variants_testing_coverage:
        if variants_testing_coverage[variant] >= filter_coverage_rate or variant in failling_variants:
            total_variants += 1
            variant_dir = get_variant_dir(mutated_project_dir, variant)
            features_info = get_coverage_infor_of_variants(variant, variant_dir, failling_variants,  features_info)

    total_passes = total_variants - len(failling_variants)
    total_fails = len(failling_variants)
    features_info = features_suspiciousness_calculation(features_info, total_passes, total_fails, ranking_type)
    feature_rank, stm_rank = search_rank(buggy_statement, features_info, ranking_type)
    search_space = total_ranking_statements(features_info)
    return feature_rank, stm_rank, search_space

def features_suspiciousness_calculation(features_info, total_passes, total_fails, ranking_type):
    for id in features_info.keys():
        if ranking_type == TARANTULA:
            features_info[id][TARANTULA_SCORE] = tarantula_calculation(len(features_info[id][VARIANTS_FAILED]),
                                                                         len(features_info[id][VARIANTS_PASSED]),
                                                                         total_fails,
                                                                         total_passes)
        elif ranking_type == OCHIAI:
            features_info[id][OCHIAI_SCORE] = ochiai_calculation(len(features_info[id][VARIANTS_FAILED]),
                                                                         len(features_info[id][VARIANTS_PASSED]),
                                                                         total_fails)
        elif ranking_type == OP2:
            features_info[id][OP2_SCORE] = op2_calculation(len(features_info[id][VARIANTS_FAILED]),
                                                                         len(features_info[id][VARIANTS_PASSED]),
                                                                         total_passes)
        elif ranking_type == BARINEL:
            features_info[id][BARINEL_SCORE] = barinel_calculation(len(features_info[id][VARIANTS_FAILED]),
                                                                         len(features_info[id][VARIANTS_PASSED]))
        elif ranking_type == DSTAR:
            features_info[id][DSTAR_SCORE] = dstar_calculation(len(features_info[id][VARIANTS_FAILED]),
                                                                         len(features_info[id][VARIANTS_PASSED]),
                                                                         total_fails)
    return features_info

def get_coverage_infor_of_variants(variant, variant_dir, failling_variants,  features_coverage_info):

    test_coverage_dir = get_test_coverage_dir(variant_dir)

    spectrum_failed_coverage_file_dir = join_path(test_coverage_dir, SPECTRUM_FAILED_COVERAGE_FILE_NAME)
    spectrum_passed_coverage_file_dir = join_path(test_coverage_dir, SPECTRUM_PASSED_COVERAGE_FILE_NAME)

    if variant in failling_variants:
        if os.path.isfile(spectrum_failed_coverage_file_dir):
            features_coverage_info = read_coverage_info(variant, features_coverage_info, spectrum_failed_coverage_file_dir, VARIANTS_FAILED)

        if os.path.isfile(spectrum_passed_coverage_file_dir):
           features_coverage_info = read_coverage_info(variant, features_coverage_info, spectrum_passed_coverage_file_dir, VARIANTS_FAILED)
    else:
        if os.path.isfile(spectrum_failed_coverage_file_dir):
            features_coverage_info = read_coverage_info(variant, features_coverage_info,
                                                        spectrum_failed_coverage_file_dir, VARIANTS_PASSED)

        if os.path.isfile(spectrum_passed_coverage_file_dir):
            features_coverage_info = read_coverage_info(variant, features_coverage_info,
                                                        spectrum_passed_coverage_file_dir, VARIANTS_PASSED)

    return features_coverage_info

def read_coverage_info(variant, coverage_info, coverage_file, kind_of_test_count):
    try:
        tree = ET.parse(coverage_file)
        root = tree.getroot()
        project = root.find("project")

        for package in project:
            for file in package:
                for line in file:
                    id = line.get('featureClass')
                    if id not in coverage_info:
                        coverage_info[id] = {}
                        coverage_info[id][VARIANTS_FAILED] = []
                        coverage_info[id][VARIANTS_PASSED] = []
                        coverage_info[id][STATEMENT_ID] = []
                    if int(line.get('count')) > 0 and variant not in coverage_info[id][kind_of_test_count]:
                        coverage_info[id][kind_of_test_count].append(variant)
                    stm_id = line.get('featureClass') + "." + line.get('featureLineNum')
                    if stm_id not in coverage_info[id][STATEMENT_ID]:
                        coverage_info[id][STATEMENT_ID].append(stm_id)
        return coverage_info
    except:
        logging.info("Exception when parsing %s", coverage_file)

def search_rank(buggy_stm, features_info, ranking_type):
    ranking_score_type = ranking_type + "_score"
    score = 0
    for feature in features_info:
        if buggy_stm in features_info[feature][STATEMENT_ID]:
            score = features_info[feature][ranking_score_type]
            break

    feature_rank = 0
    stm_rank = 0
    for feature in features_info:
        if features_info[feature][ranking_score_type] >= score:
            feature_rank += 1
            stm_rank += len(features_info[feature][STATEMENT_ID])
    return feature_rank, stm_rank

def total_ranking_statements(features_info):
    stms = 0
    for feature in features_info:
        stms += len(features_info[feature][STATEMENT_ID])
    return stms


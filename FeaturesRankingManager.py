import logging
import os

import xml.etree.ElementTree as ET

from FileManager import get_variant_dir, get_test_coverage_dir, join_path, \
    SPECTRUM_FAILED_COVERAGE_FILE_NAME, SPECTRUM_PASSED_COVERAGE_FILE_NAME
from RankingManager import WORST_CASE

from Spectrum_Expression import tarantula_calculation, ochiai_calculation, op2_calculation, barinel_calculation, \
    dstar_calculation, TARANTULA_SCORE, TARANTULA, OCHIAI, OCHIAI_SCORE, OP2, OP2_SCORE, BARINEL, BARINEL_SCORE, DSTAR, \
    DSTAR_SCORE, RUSSELL_RAO, RUSSELL_RAO_SCORE, russell_rao_calculation, SIMPLE_MATCHING, simple_matching_calculation, \
    ROGERS_TANIMOTO_SCORE, SIMPLE_MATCHING_SCORE, ROGERS_TANIMOTO, rogers_tanimoto_calculation, AMPLE, AMPLE_SCORE, \
    ample_calculation, JACCARD_SCORE, JACCARD, jaccard_calculation, COHEN, COHEN_SCORE, cohen_calculation, SCOTT, \
    SCOTT_SCORE, scott_calculation, ROGOT1, ROGOT1_SCORE, rogot1_calculation, GEOMETRIC_MEAN, GEOMETRIC_MEAN_SCORE, \
    geometric_mean_calculation, M2, M2_SCORE, m2_calculation

from TestingCoverageManager import statement_coverage_of_variants

STATEMENT_ID = "stm_id"
VARIANTS_FAILED = "variants_failed"
VARIANTS_PASSED = "variants_passed"

def features_ranking(buggy_statement, mutated_project_dir, failling_variants, filter_coverage_rate, spectrum_expression, rank_type):
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
    features_info = features_suspiciousness_calculation(features_info, total_passes, total_fails, spectrum_expression)
    if rank_type == WORST_CASE:
        feature_rank, stm_rank = search_rank_worst_case(buggy_statement, features_info, spectrum_expression)
    else:
        feature_rank, stm_rank = search_rank_best_case(buggy_statement, features_info, spectrum_expression)

    search_space = total_ranking_statements(features_info)
    return feature_rank, stm_rank, search_space

def features_suspiciousness_calculation(features_info, total_passes, total_fails, spectrum_expression):
    for id in features_info.keys():
        if spectrum_expression == TARANTULA:
            features_info[id][TARANTULA_SCORE] = tarantula_calculation(len(features_info[id][VARIANTS_FAILED]),
                                                                         len(features_info[id][VARIANTS_PASSED]),
                                                                         total_fails,
                                                                         total_passes)
        elif spectrum_expression == OCHIAI:
            features_info[id][OCHIAI_SCORE] = ochiai_calculation(len(features_info[id][VARIANTS_FAILED]),
                                                                         len(features_info[id][VARIANTS_PASSED]),
                                                                         total_fails)
        elif spectrum_expression == OP2:
            features_info[id][OP2_SCORE] = op2_calculation(len(features_info[id][VARIANTS_FAILED]),
                                                                         len(features_info[id][VARIANTS_PASSED]),
                                                                         total_passes)
        elif spectrum_expression == BARINEL:
            features_info[id][BARINEL_SCORE] = barinel_calculation(len(features_info[id][VARIANTS_FAILED]),
                                                                         len(features_info[id][VARIANTS_PASSED]))
        elif spectrum_expression == DSTAR:
            features_info[id][DSTAR_SCORE] = dstar_calculation(len(features_info[id][VARIANTS_FAILED]),
                                                                         len(features_info[id][VARIANTS_PASSED]),
                                                                         total_fails)
        elif spectrum_expression == DSTAR:
            features_info[id][DSTAR_SCORE] = dstar_calculation(len(features_info[id][VARIANTS_FAILED]),
                                                                         len(features_info[id][VARIANTS_PASSED]),
                                                                         total_fails)
        elif spectrum_expression == RUSSELL_RAO:
            features_info[id][RUSSELL_RAO_SCORE] = russell_rao_calculation(len(features_info[id][VARIANTS_FAILED]),
                                                                 total_fails, total_passes)
        elif spectrum_expression == SIMPLE_MATCHING:
            features_info[id][SIMPLE_MATCHING_SCORE] = simple_matching_calculation(len(features_info[id][VARIANTS_FAILED]), len(features_info[id][VARIANTS_PASSED]),
                                                                 total_fails, total_passes)
        elif spectrum_expression == ROGERS_TANIMOTO:
            features_info[id][ROGERS_TANIMOTO_SCORE] = rogers_tanimoto_calculation(len(features_info[id][VARIANTS_FAILED]), len(features_info[id][VARIANTS_PASSED]),
                                                                 total_fails, total_passes)
        elif spectrum_expression == AMPLE:
            features_info[id][AMPLE_SCORE] = ample_calculation(len(features_info[id][VARIANTS_FAILED]), len(features_info[id][VARIANTS_PASSED]),
                                                                 total_fails, total_passes)
        elif spectrum_expression == JACCARD:
            features_info[id][JACCARD_SCORE] = jaccard_calculation(len(features_info[id][VARIANTS_FAILED]), len(features_info[id][VARIANTS_PASSED]),
                                                                 total_fails)
        elif spectrum_expression == COHEN:
            features_info[id][COHEN_SCORE] = cohen_calculation(len(features_info[id][VARIANTS_FAILED]), len(features_info[id][VARIANTS_PASSED]),
                                                                 total_fails, total_passes)
        elif spectrum_expression == SCOTT:
            features_info[id][SCOTT_SCORE] = scott_calculation(len(features_info[id][VARIANTS_FAILED]), len(features_info[id][VARIANTS_PASSED]),
                                                                 total_fails, total_passes)
        elif spectrum_expression == ROGOT1:
            features_info[id][ROGOT1_SCORE] = rogot1_calculation(len(features_info[id][VARIANTS_FAILED]), len(features_info[id][VARIANTS_PASSED]),
                                                                 total_fails, total_passes)
        elif spectrum_expression == GEOMETRIC_MEAN:
            features_info[id][GEOMETRIC_MEAN_SCORE] = geometric_mean_calculation(len(features_info[id][VARIANTS_FAILED]), len(features_info[id][VARIANTS_PASSED]),
                                                                 total_fails, total_passes)
        elif spectrum_expression == M2:
            features_info[id][M2_SCORE] = m2_calculation(len(features_info[id][VARIANTS_FAILED]), len(features_info[id][VARIANTS_PASSED]),
                                                                 total_fails, total_passes)
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

def search_rank_worst_case(buggy_stm, features_info, spectrum_expression):
    ranking_score_type = spectrum_expression + "_score"
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

def search_rank_best_case(buggy_stm, features_info, spectrum_expression):
    ranking_score_type = spectrum_expression + "_score"
    score = 0
    for feature in features_info:
        if buggy_stm in features_info[feature][STATEMENT_ID]:
            score = features_info[feature][ranking_score_type]
            break

    feature_rank = 0
    stm_rank = 0
    for feature in features_info:
        if features_info[feature][ranking_score_type] > score:
            feature_rank += 1
            stm_rank += len(features_info[feature][STATEMENT_ID])
    return feature_rank + 1, stm_rank + 1


def total_ranking_statements(features_info):
    stms = 0
    for feature in features_info:
        stms += len(features_info[feature][STATEMENT_ID])
    return stms


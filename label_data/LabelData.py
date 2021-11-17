from label_data.HelperForLabeledData import *
from suspicious_statements_manager.SuspiciousStatementManager import get_multiple_buggy_statements, get_mutated_features
import csv
import xml.etree.ElementTree as ET
from FileManager import *
import logging


def passing_product_has_buggy_features(config_file, buggy_features):
    passing_products = []
    with open(config_file) as csv_file:
        csv_reader = csv.reader(csv_file)
        count = 0
        buggy_indexs = []
        for row in csv_reader:
            if count == 0:
                for f in buggy_features:
                    buggy_indexs.append(row.index(f))
                count += 1
            elif "PASS" in row[-1]:
                for index in buggy_indexs:
                    if "T" in row[index]:
                        passing_products.append(row[0])
    return passing_products


def read_info(coverage_file):
    statement_infor = []
    try:
        tree = ET.parse(coverage_file)
        root = tree.getroot()
        project = root.find("project")

        for package in project:
            for file in package:
                for line in file:
                    id = line.get('featureClass') + "." + line.get('featureLineNum')
                    if id not in statement_infor:
                        statement_infor.append(id)
        return statement_infor
    except:
        logging.info("Exception when parsing %s", coverage_file)


def passing_product_has_buggy_statements(mutated_project_dir, passing_variants, buggy_statements):
    variants_dir = get_variants_dir(mutated_project_dir)
    variants = []
    for v in passing_variants:
        passing_test_coverage = join_path(get_test_coverage_dir(join_path(variants_dir, v)),
                                          SPECTRUM_PASSED_COVERAGE_FILE_NAME)
        statements_set = read_info(passing_test_coverage)
        for b in buggy_statements:
            if b in statements_set:
                variants.append(v)
    return variants


def base_is_buggy_features(base_features, buggy_features):
    for base in base_features:
        if base in buggy_features:
            return True
    return False


def verify_failing_variants(mutated_project_dir):
    buggy_stmts = get_multiple_buggy_statements(mutated_project_dir.split("/")[-1], mutated_project_dir)
    failing_variants = get_failing_variants(mutated_project_dir)
    system_stm_ids = get_all_stm_ids(mutated_project_dir)
    failing_executions = get_failings_executions(mutated_project_dir, system_stm_ids, failing_variants)
    unconverted_to_FP_variants = []
    for bstm in buggy_stmts:
        flag = False
        for v in failing_executions:
            for test in failing_executions[v]:
                for item in failing_executions[v][test]:
                    if item['id'] == bstm:
                        flag = True
                        if v not in unconverted_to_FP_variants:
                            unconverted_to_FP_variants.append(v)
                        break
                if flag: break
            if flag: break
    return unconverted_to_FP_variants


def label(mutated_project_dir, passing_variants_contain_buggy_stmts):
    variants_dir = get_variants_dir(mutated_project_dir)
    variants = list_dir(variants_dir)
    failing_variants = get_failing_variants(mutated_project_dir)
    unconverted_to_FP_variants = verify_failing_variants(mutated_project_dir)
    file_name = join_path(mutated_project_dir, LABELED_FILE_NAME)
    verify_failing_variants(mutated_project_dir)
    with open(file_name, 'w', newline='') as csvfile:
        fieldnames = ['VARIANT', 'LABEL', 'FP created from F']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for v in variants:
            if v in failing_variants:
                v_index = failing_variants.index(v)
                if v_index % 2 == 0:
                    writer.writerow({'VARIANT': v, 'LABEL': FAILING})
                elif v not in unconverted_to_FP_variants:
                    writer.writerow({'VARIANT': v, 'LABEL': FALSE_PASSING, 'FP created from F': '1'})
            elif v in passing_variants_contain_buggy_stmts:
                writer.writerow({'VARIANT': v, 'LABEL': FALSE_PASSING})
            else:
                writer.writerow({'VARIANT': v, 'LABEL': TRUE_PASSING})

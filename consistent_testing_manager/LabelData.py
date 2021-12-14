from consistent_testing_manager.FPMatricsCaculation import *
from consistent_testing_manager.FileName import variants_testing_label_file
from spectrum_manager.SpectrumReader import get_all_stm_ids, get_failings_executions
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
        if not flag:
            unconverted_to_FP_variants.append("-1")
    return unconverted_to_FP_variants


def label(mutated_project_dir, passing_variants_contain_buggy_stmts):
    variants_dir = get_variants_dir(mutated_project_dir)
    variants = list_dir(variants_dir)
    failing_variants = get_failing_variants(mutated_project_dir)
    unconverted_to_FP_variants = verify_failing_variants(mutated_project_dir)
    for item in unconverted_to_FP_variants:
        if item == "-1":
            print(mutated_project_dir)
            return
    file_name = join_path(mutated_project_dir, LABELED_FILE_NAME)
    num_failings = 0
    num_fp = 0
    num_tp = 0
    with open(file_name, 'w', newline='') as csvfile:
        fieldnames = ['VARIANT', 'LABEL', 'FP created from F']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for v in variants:
            if v in failing_variants:
                v_index = failing_variants.index(v)
                if v_index % 2 == 0:
                    writer.writerow({'VARIANT': v, 'LABEL': FAILING})
                    num_failings += 1
                else:
                    if v not in unconverted_to_FP_variants:
                        writer.writerow({'VARIANT': v, 'LABEL': FALSE_PASSING, 'FP created from F': '1'})
                        num_fp += 1
                    else:
                        writer.writerow({'VARIANT': v, 'LABEL': FAILING})
                        num_failings += 1
            elif v in passing_variants_contain_buggy_stmts:
                writer.writerow({'VARIANT': v, 'LABEL': FALSE_PASSING})
                num_fp += 1
            else:
                writer.writerow({'VARIANT': v, 'LABEL': TRUE_PASSING})
                num_tp += 1
    if num_failings == 0 or num_tp == 0 or num_fp == 0:
        os.remove(file_name)


def label_data(system_paths):
    logfile = open("statistics/contain_buggy_features_but_not_buggy_stmts.txt", "w")
    base_features = ["BankAccount", "Base", "ExamDB", "Compress"]
    for system in system_paths:
        for bug in system_paths[system]:
            sys_path = system_paths[system][bug]
            logfile.write(sys_path + "\n")
            mutated_projects = list_dir(sys_path)
            for mutated_project in mutated_projects:
                mu_project_path = join_path(sys_path, mutated_project)
                buggy_stmts = get_multiple_buggy_statements(mutated_project, mu_project_path)
                buggy_features = get_mutated_features(mu_project_path)
                config_report_path = get_model_configs_report_path(mu_project_path)
                failing_variants = get_failing_variants(mu_project_path)

                if not base_is_buggy_features(base_features, buggy_features):
                    passing_variants_contain_buggy_features = passing_product_has_buggy_features(config_report_path,
                                                                                                 buggy_features)

                    passing_variants_contain_buggy_stmts = passing_product_has_buggy_statements(mu_project_path,
                                                                                                passing_variants_contain_buggy_features,
                                                                                                buggy_stmts)
                    if len(passing_variants_contain_buggy_features) > 0 and len(
                            passing_variants_contain_buggy_stmts) == 0 and len(failing_variants) != 1:
                        logfile.write(mutated_project + "\n")

                    if not (len(failing_variants) == 1 and len(passing_variants_contain_buggy_stmts) == 0):
                        label(mu_project_path, passing_variants_contain_buggy_stmts)

    logfile.close()


def do_label_statistics(system_paths):
    logfile = open("statistics/labels_in_systems.txt", "w")
    for system in system_paths:
        for bug in system_paths[system]:
            sys_path = system_paths[system][bug]
            logfile.write(sys_path + "\n")
            mutated_projects = list_dir(sys_path)
            sum_f = 0
            sum_tp = 0
            sum_fp = 0
            total_cases = 0
            for mutated_project in mutated_projects:
                mu_project_path = join_path(sys_path, mutated_project)
                label_file = join_path(mu_project_path, variants_testing_label_file)
                if os.path.isfile(label_file):
                    with open(label_file) as csv_file:
                        csv_reader = csv.reader(csv_file, delimiter=',')
                        for row in csv_reader:
                            if row[1] == FAILING:
                                sum_f += 1
                            elif row[1] == FALSE_PASSING:
                                sum_fp += 1
                            elif row[1] == TRUE_PASSING:
                                sum_tp += 1
                    total_cases += 1
            logfile.write("total labeled cases: " + str(total_cases) + "\n")
            logfile.write("num of failing variants: " + str(sum_f / total_cases) + "\n")
            logfile.write("num of false passing variants: " + str(sum_fp / total_cases) + "\n")
            logfile.write("num of true passing variants: " + str(sum_tp / total_cases) + "\n")
    logfile.close()

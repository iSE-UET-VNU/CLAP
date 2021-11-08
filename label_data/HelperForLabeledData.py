import csv

from FileManager import *
from label_data.LabelData import *
from FileManager import *
import xml.etree.ElementTree as ET

from ranking.MultipleBugsManager import get_suspicious_space
from ranking.RankingManager import get_infor_for_sbfl, get_set_of_stms, sbfl_ranking, SS_STMS_IN_F_PRODUCTS
from ranking.Spectrum_Expression import OP2

TRUE_PASSING = "TP"
FALSE_PASSING = "FP"
FAILING = "F"
LABELED_FILE_NAME = "variants_testing_label.csv"

VARIANT_NAME = 'VARIANT'
LABEL = 'LABEL'
CREATED_FP = 'FP created from F'
DDU = "DDU"

executed_susp_stmt_vs_susp_stmt_in_passing_variant = "executed_susp_stmt_vs_susp_stmt_in_passing_variant"
not_executed_susp_stmt_vs_susp_stmt_in_passing_variant = "not_executed_susp_stmt_vs_susp_stmt_in_passing_variant"
executed_susp_stmt_vs_susp_stmt_in_a_failed_execution = "executed_susp_stmt_vs_susp_stmt_in_a_failed_execution"
not_executed_susp_stmt_vs_susp_stmt_in_a_failed_execution = "not_executed_susp_stmt_vs_susp_stmt_in_a_failed_execution"
tested_unexpected_behaviors_in_passing_variant = "tested_unexpected_behaviors_in_passing_variant"
confirmed_successes_in_passing_variant = "check_confirmed_successes_in_passing_variant"
total_susp_scores = "total_susp_scores"


def get_variants_and_labels(mutated_project_dir):
    variants = {}
    label_file = join_path(mutated_project_dir, LABELED_FILE_NAME)
    with open(label_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            variants[row[VARIANT_NAME]] = {LABEL: row[LABEL], CREATED_FP: row[CREATED_FP]}
    return variants


def write_dict_to_file(file_name, data, fieldnames):
    with open(file_name, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for item in data:
            tmp = {}
            for f in fieldnames:
                if fieldnames.index(f) == 0:
                    tmp[f] = item
                else:
                    tmp[f] = data[item][f]
            writer.writerow(tmp)


def get_stm_ids_per_variant(variant_dir):
    coverage_dir = get_test_coverage_dir(variant_dir)
    spectrum_dirs = [join_path(coverage_dir, SPECTRUM_FAILED_COVERAGE_FILE_NAME),
                     join_path(coverage_dir, SPECTRUM_PASSED_COVERAGE_FILE_NAME)]
    data = {}
    for cfile in spectrum_dirs:
        if os.path.isfile(cfile):
            try:
                tree = ET.parse(cfile)
                root = tree.getroot()
                project = root.find("project")
                for package in project:
                    for file in package:
                        file_name = file.get("path")
                        for line in file:
                            id = line.get('featureClass') + "." + line.get('featureLineNum')
                            key = file_name + "." + line.get('num')
                            if key not in data:
                                data[key] = {}
                                data[key]['id'] = id
                                data[key]['tested'] = 0
                                if int(line.get('count')) != 0:
                                    data[key]['tested'] = 1;
            except:
                logging.info("Exception when parsing %s", cfile)
    return data


def get_all_stm_ids(project_dir):
    system_stm_ids = {}
    variants = get_all_variant_dirs(project_dir)
    for variant in variants:
        variant_name = variant.split("/")[-1]
        system_stm_ids[variant_name] = get_stm_ids_per_variant(variant)
    return system_stm_ids


def read_coverage_file(system_stm_ids, coverage_file_dir):
    data = []
    if os.path.isfile(coverage_file_dir):
        try:
            tree = ET.parse(coverage_file_dir)
            root = tree.getroot()
            project = root.find("project")
            packages = project.findall("package")
            for package in packages:
                files = package.findall("file")
                for file in files:
                    file_path = file.get("path").split("/")
                    src_id = file_path.index("src")
                    file_name = "/".join(file_path[src_id + 1:])
                    lines = file.findall("line")
                    for line in lines:
                        id = file_name + "." + line.get('num')
                        if "count" in line.attrib and int(line.get("count")) > 0:
                            if id in system_stm_ids.keys():
                                if system_stm_ids[id] not in data:
                                    data.append(system_stm_ids[id])
        except:
            logging.info("Exception when parsing %s", coverage_file_dir)
    return data


def get_failings_executions(project_dir, system_stm_ids, failing_variants):
    failed_test_executions = {}
    for variant in failing_variants:
        failed_test_executions[variant] = {}
        variant_dir = get_variant_dir(project_dir, variant)
        failed_tests_coverage_dir = get_failed_test_coverage_dir(variant_dir)
        all_failed_spectrums = list_dir(failed_tests_coverage_dir)
        for file in all_failed_spectrums:
            file_dir = join_path(failed_tests_coverage_dir, file)
            failed_test_executions[variant][file] = read_coverage_file(system_stm_ids[variant], file_dir)
    return failed_test_executions


def get_passing_executions(project_dir, system_stm_ids, variants):
    passed_test_executions = {}
    for variant in variants:
        passed_test_executions[variant] = {}
        variant_dir = get_variant_dir(project_dir, variant)
        passed_tests_coverage_dir = get_passed_test_coverage_dir(variant_dir)
        all_passed_spectrums = list_dir(passed_tests_coverage_dir)
        for file in all_passed_spectrums:
            file_dir = join_path(passed_tests_coverage_dir, file)
            passed_test_executions[variant][file] = read_coverage_file(system_stm_ids[variant], file_dir)
    return passed_test_executions


def get_passing_executions_in_a_variant(project_dir, system_stm_ids, variant):
    passed_test_executions = {}
    variant_dir = get_variant_dir(project_dir, variant)
    passed_tests_coverage_dir = get_passed_test_coverage_dir(variant_dir)
    all_passed_spectrums = list_dir(passed_tests_coverage_dir)
    for file in all_passed_spectrums:
        file_dir = join_path(passed_tests_coverage_dir, file)
        passed_test_executions[file] = read_coverage_file(system_stm_ids[variant], file_dir)
    return passed_test_executions


def get_labeled_failing_variants(project_dir):
    failing_variants = get_failing_variants(project_dir)
    variants_and_labels = get_variants_and_labels(project_dir)
    for item in failing_variants:
        if variants_and_labels[item][LABEL] != FAILING:
            failing_variants.remove(item)
    return failing_variants


def get_stmts_id_in_passing_variants(project_dir, failing_variants):
    passing_variants_stmts = {}
    variants_dir = get_variants_dir(project_dir)
    variants_list = list_dir(variants_dir)
    for variant in variants_list:
        if variant not in failing_variants:
            variant_dir = join_path(variants_dir, variant)
            variant_stmts = get_stm_ids_per_variant(variant_dir)
            passing_variants_stmts[variant] = variant_stmts
    return passing_variants_stmts


def convert_to_dict(passing_variant_stmt):
    stmt_ids = {}
    for item in passing_variant_stmt:
        tmp = passing_variant_stmt[item]

        if tmp["id"] not in stmt_ids:
            stmt_ids[tmp["id"]] = {}
            stmt_ids[tmp["id"]]["tested"] = tmp["tested"]
    return stmt_ids


def similar_path(path1, path2, threshold):
    count = 0
    for item in path1:
        if item in path2:
            count += 1
    if count / len(path1) > threshold:
        return True
    return False


def exist_path(path, list_paths, threshold):
    for p in list_paths:
        if similar_path(path, list_paths[p], threshold):
            return True
    return False


def check_suspicious_stmts_in_passing_variants(failing_exections, passing_variant_stmt):
    passing_variant_stmt_dict = convert_to_dict(passing_variant_stmt)
    suspicious_in_passing_variant = {}
    for variant_name in failing_exections:
        for test in failing_exections[variant_name]:
            execution = failing_exections[variant_name][test]
            D1 = []
            D2 = []
            for item in execution:
                if item["id"] in passing_variant_stmt_dict:
                    if passing_variant_stmt_dict[item["id"]]["tested"] == 1:
                        D1.append(item["id"])
                    else:
                        D2.append(item["id"])
            suspicious_in_passing_variant[variant_name + "__" + test] = {"Executed": D1, "Not Executed": D2}

    return suspicious_in_passing_variant


def check_executed_susp_stmt_vs_susp_stmt_in_passing_variant(susp_in_passing_variant):
    min = 1000
    for item in susp_in_passing_variant:
        executed_set_len = len(susp_in_passing_variant[item]["Executed"])
        suspicious_set_len = len(susp_in_passing_variant[item]["Not Executed"]) + executed_set_len
        if suspicious_set_len == 0:
            if min < 0:
                min = 1
        else:
            tmp = executed_set_len / suspicious_set_len
            if tmp < min:
                min = tmp
    return 1 - min


def check_not_executed_susp_stmt_vs_susp_stmt_in_passing_variant(susp_in_passing_variant):
    max = -1000
    for item in susp_in_passing_variant:
        not_executed_set_len = len(susp_in_passing_variant[item]["Not Executed"])
        suspicious_set_len = len(susp_in_passing_variant[item]["Executed"]) + not_executed_set_len
        if suspicious_set_len == 0:
            if max < 0:
                max = 0
        else:
            tmp = not_executed_set_len / suspicious_set_len
            if tmp > max:
                max = tmp
    return max


def check_executed_susp_stmt_vs_susp_stmt_in_a_failed_execution(failed_excutions, susp_in_passing_variant):
    max = -1000
    for item in susp_in_passing_variant:
        var_name = item.split("__")[0]
        test_id = item.split("__")[1]
        failed_execution_len = len(failed_excutions[var_name][test_id])
        susp_executed_set_len = len(susp_in_passing_variant[item]["Executed"])
        if failed_execution_len != 0:
            if susp_executed_set_len / failed_execution_len > max:
                max = susp_executed_set_len / failed_execution_len

    return max


def check_not_executed_susp_stmt_vs_susp_stmt_in_a_failed_execution(failed_excutions, susp_in_passing_variant):
    max = -1000
    for item in susp_in_passing_variant:
        var_name = item.split("__")[0]
        test_id = item.split("__")[1]
        failed_execution_len = len(failed_excutions[var_name][test_id])
        not_susp_executed_set_len = len(susp_in_passing_variant[item]["Not Executed"])
        if failed_execution_len != 0:
            if not_susp_executed_set_len / failed_execution_len > max:
                max = not_susp_executed_set_len / failed_execution_len

    return max


def check_tested_unexpected_behaviors_in_passing_variant(executions_in_failing_products, execution_in_a_passing_product,
                                                         susp_in_passing_product,
                                                         threshold):
    num_failed_executions_contained_in_passing_product = 0
    num_failed_exeuctions_tested_by_passing_product = 0
    for item in susp_in_passing_product:
        var_name = item.split("__")[0]
        test_id = item.split("__")[1]
        failed_execution = executions_in_failing_products[var_name][test_id]
        susp_set_len = len(susp_in_passing_product[item]["Executed"]) + len(
            susp_in_passing_product[item]["Not Executed"])
        if susp_set_len / len(failed_execution) > threshold:
            num_failed_executions_contained_in_passing_product += 1
            if exist_path(failed_execution, execution_in_a_passing_product, threshold):
                num_failed_exeuctions_tested_by_passing_product += 1

    if num_failed_executions_contained_in_passing_product == 0:
        return 0
    else:
        return 1 - num_failed_exeuctions_tested_by_passing_product / num_failed_executions_contained_in_passing_product


def check_confirmed_successes_in_passing_variant(executions_in_failing_products, passed_executions_in_failing_products,
                                                 passed_executions_in_passing_product, susp_in_passing_product,
                                                 threshold):
    fvars_have_susp_in_pvariant = []
    for item in susp_in_passing_product:
        var_name = item.split("__")[0]
        test_id = item.split("__")[1]
        failed_execution = executions_in_failing_products[var_name][test_id]
        susp_set_len = len(susp_in_passing_product[item]["Executed"]) + len(
            susp_in_passing_product[item]["Not Executed"])
        if susp_set_len / len(failed_execution) >= threshold:
            if (var_name not in fvars_have_susp_in_pvariant):
                fvars_have_susp_in_pvariant.append(var_name)
    sum = 0

    for fvariant in fvars_have_susp_in_pvariant:
        covered_susscesses = 0
        for test in passed_executions_in_passing_product:
            if exist_path(passed_executions_in_passing_product[test],
                          passed_executions_in_failing_products[fvariant], threshold):
                covered_susscesses += 1
        sum += covered_susscesses / len(passed_executions_in_passing_product)
    if len(fvars_have_susp_in_pvariant) == 0:
        return 0
    else:
        return 1 - sum / len(fvars_have_susp_in_pvariant)


def ranking_suspicious_stmts(project_dir):
    search_spaces = get_suspicious_space(project_dir, 0.0, "")
    stm_info_for_sbfl, total_passed_tests, total_failed_tests = get_infor_for_sbfl(project_dir,
                                                                                   "",
                                                                                   0.0)
    all_stms_f_products_set = get_set_of_stms(search_spaces[SS_STMS_IN_F_PRODUCTS])
    full_ranked_list = sbfl_ranking(stm_info_for_sbfl, total_failed_tests, total_passed_tests,
                                    all_stms_f_products_set,
                                    [OP2])
    op2_ranked_list = {}
    for (stmt, score, v) in full_ranked_list[OP2]:
        op2_ranked_list[stmt] = score

    return op2_ranked_list


def check_total_susp_scores_in_passing_variant(susp_scores, passing_variant_stmt):
    sum_scores = 0
    for stmt in passing_variant_stmt:
        tmp = passing_variant_stmt[stmt]["id"]
        if tmp in susp_scores:
           sum_scores += susp_scores[tmp]
    return sum_scores

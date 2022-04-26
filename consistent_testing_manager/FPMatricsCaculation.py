import csv
import json
from collections import defaultdict

import pandas
from sklearn import preprocessing
from FileManager import *
from consistent_testing_manager.DDU import ddu

from spectrum_manager.SpectrumReader import get_stm_ids_per_variant, similar_path, \
    get_suspicious_space_consistent_version, get_infor_for_sbfl, get_passing_executions_in_a_variant, \
    get_failings_executions, get_passing_executions, get_all_stm_ids
from ranking.RankingManager import get_set_of_stms, sbfl_ranking
from spectrum_manager.Spectrum_Expression import OCHIAI

BACKWARD_SLICING_TYPE = "Backward"
FORWARD_SLICING_TYPE = "Forward"
BOTH_FB_SLICING_TYPE = "Both"

TRUE_PASSING = "TP"
FALSE_PASSING = "FP"
FAILING = "F"

VARIANT_NAME = 'VARIANT'
LABEL = 'LABEL'
TRANSFORMED_FP = 'FP transformed from F'
DDU = "DDU"

buggy_statement_containing_possibility = "bscp"
executed_susp_stmt_in_passing_variant = "executed_susp_stmt_in_passing_variant"
code_coverage = "code_coverage"

incorrectness_verifiability = "incorrectness_verifiability"
correctness_reflectability = "correctness_reflectability"

bug_involving_statements = "bug_involving_statements"


def get_variants_and_labels(mutated_project_dir, label_file):
    variants = {}
    label_file = join_path(mutated_project_dir, label_file)
    with open(label_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            variants[row[VARIANT_NAME]] = {LABEL: row[LABEL], TRANSFORMED_FP: row[TRANSFORMED_FP]}
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


def get_labeled_failing_variants(project_dir, label_file):
    failing_variants = get_failing_variants(project_dir)
    variants_and_labels = get_variants_and_labels(project_dir, label_file)
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
            variant_stmts = get_stm_ids_per_variant(variant_dir, fp_variant=True)
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


def convert_execution_to_set(execution):
    execution_set = set()
    for item in execution:
        execution_set.add(item["id"])
    return execution_set


def exist_path(path, list_paths, threshold):
    for p in list_paths:
        if similar_path(path, list_paths[p], threshold):
            return True
    return False


def check_suspicious_stmts_in_passing_variants(failing_executions, passing_variant_stmt):
    passing_variant_stmt_dict = convert_to_dict(passing_variant_stmt)
    suspicious_in_passing_variant = {}
    for variant_name in failing_executions:
        for test in failing_executions[variant_name]:
            execution = failing_executions[variant_name][test]
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
    executed_suspicious_stmt = set()
    not_executed_suspcious_stmt = set()
    for item in susp_in_passing_variant:
        executed_suspicious_stmt.update(susp_in_passing_variant[item]["Executed"])
        not_executed_suspcious_stmt.update(susp_in_passing_variant[item]["Not Executed"])
    for item in executed_suspicious_stmt:
        not_executed_suspcious_stmt.discard(item)

    total_suspicious_stmts = len(executed_suspicious_stmt) + len(not_executed_suspcious_stmt)
    if total_suspicious_stmts == 0:
        return 0, 0
    return len(not_executed_suspcious_stmt)/total_suspicious_stmts


def jaccard_similarity(set1, set2):
    interaction = len(set1.intersection(set2))
    union = len(set1) + len(set2) - interaction
    if union == 0:
        return 0
    return float(interaction) / union


def check_incorrectness_verifiability(executions_in_failing_products, execution_in_a_passing_product,
                                      susp_in_passing_product,
                                      threshold):
    num_failed_executions_contained_in_passing_product = 0
    num_failed_executions_tested_by_passing_product = 0
    for item in susp_in_passing_product:
        var_name = item.split("__")[0]
        test_id = item.split("__")[1]
        failed_execution = executions_in_failing_products[var_name][test_id]
        susp_set_len = len(susp_in_passing_product[item]["Executed"]) + len(
            susp_in_passing_product[item]["Not Executed"])
        if susp_set_len / len(failed_execution) > threshold:
            num_failed_executions_contained_in_passing_product += 1
            if exist_path(failed_execution, execution_in_a_passing_product, threshold):
                num_failed_executions_tested_by_passing_product += 1

    if num_failed_executions_contained_in_passing_product == 0:
        return 0
    else:
        return 1 - num_failed_executions_tested_by_passing_product / num_failed_executions_contained_in_passing_product


def check_correctness_reflectability(failed_executions_in_failing_products,
                                     passed_executions_in_failing_products,
                                     passed_executions_in_passing_product, susp_in_passing_product,
                                     threshold):
    failing_set_in_failing_variants = []
    for variant in failed_executions_in_failing_products:
        for path in failed_executions_in_failing_products[variant]:
            set_tmp = convert_execution_to_set(failed_executions_in_failing_products[variant][path])
            failing_set_in_failing_variants.append(set_tmp)

    passing_set_in_failing_variants = []
    for variant in passed_executions_in_failing_products:
        for path in passed_executions_in_failing_products[variant]:
            set_tmp = convert_execution_to_set(passed_executions_in_failing_products[variant][path])
            passing_set_in_failing_variants.append(set_tmp)

    coincidentally_passed_tests = []
    for passed in passing_set_in_failing_variants:
        for failed in failing_set_in_failing_variants:
            if jaccard_similarity(passed, failed) > threshold:
                if passed not in coincidentally_passed_tests:
                    coincidentally_passed_tests.append(passed)

    count = 0
    for path in passed_executions_in_passing_product:
        set_tmp = convert_execution_to_set(passed_executions_in_passing_product[path])
        for p_temp in coincidentally_passed_tests:
            if jaccard_similarity(set_tmp, p_temp) > threshold:
                count += 1
                break
    return count / len(passed_executions_in_passing_product)


def ranking_suspicious_stmts(project_dir, failing_variants):
    search_spaces = get_suspicious_space_consistent_version(project_dir, failing_variants, 0.0, "")
    variants = list_dir(get_variants_dir(project_dir))
    fp_variants = []
    for v in variants:
        if v not in failing_variants:
            fp_variants.append(v)
    stm_info_for_sbfl, total_passed_tests, total_failed_tests = get_infor_for_sbfl(
        project_dir, failing_variants=failing_variants, fp_variants=fp_variants,
        spectrum_coverage_prefix="",
        coverage_rate=0.0)
    all_stms_f_products_set = get_set_of_stms(search_spaces)
    full_ranked_list = sbfl_ranking(stm_info_for_sbfl, total_failed_tests, total_passed_tests,
                                    all_stms_f_products_set,
                                    [OCHIAI])
    op2_ranked_list = {}
    for (stmt, score, v) in full_ranked_list[OCHIAI]:
        op2_ranked_list[stmt] = score
    return op2_ranked_list


def check_total_susp_scores_in_passing_variant(susp_scores, passing_variant_stmt):
    sum_scores = 0
    num_of_stm = 0
    for stmt in passing_variant_stmt:
        tmp = passing_variant_stmt[stmt]["id"]
        if tmp in susp_scores:
            sum_scores += susp_scores[tmp]
            num_of_stm += 1
    if num_of_stm == 0:
        return 0
    return sum_scores / num_of_stm


def get_dependencies(slicing_file_dir):
    slicing_file = open(slicing_file_dir, "r")
    slicing_content = slicing_file.readline()
    slicies = json.loads(slicing_content)
    return slicies


def check_dependencies_by_slicing_type(similarities, susp_stmt, fv_slicies, pv_slicies, slicing_type):
    if susp_stmt in fv_slicies:
        if susp_stmt in pv_slicies:
            simi_score = jaccard_similarity(set(pv_slicies[susp_stmt]), set(fv_slicies[susp_stmt]))
            if susp_stmt not in similarities:
                similarities[susp_stmt] = {}
                similarities[susp_stmt]["Backward"] = 0
                similarities[susp_stmt]["Forward"] = 0
                similarities[susp_stmt]["Both"] = 0

            if simi_score > similarities[susp_stmt][slicing_type]:
                similarities[susp_stmt][slicing_type] = simi_score
    return similarities


def aggregate_similarity_by_avg(similarity):
    fw = 0
    bw = 0
    both = 0
    for stmt in similarity:
        fw += similarity[stmt]["Forward"]
        bw += similarity[stmt]["Backward"]
        both += similarity[stmt]["Both"]

    if len(similarity) == 0:
        return {"Forward": 0, "Backward": 0, "Both": 0}
    return {"Forward": fw / len(similarity), "Backward": bw / len(similarity), "Both": both / len(similarity)}


def concat_slicies(forward_slicies, backward_slicies):
    both_slicies = defaultdict(dict)
    for item in forward_slicies:
        both_slicies[item] = set(forward_slicies[item])

    for item in backward_slicies:
        if item not in both_slicies:
            both_slicies[item] = set(backward_slicies[item])
        else:
            both_slicies[item].update(backward_slicies[item])
    return both_slicies


def check_dependencies(variants_folder_dir, passing_variant, failed_executions_in_failing_products):
    passing_variant_dir = join_path(variants_folder_dir, passing_variant)
    pv_forward_file = get_forward_slicing_file(passing_variant_dir)
    pv_forward_slicies = get_dependencies(pv_forward_file)

    pv_backward_file = get_backward_slicing_file(passing_variant_dir)
    pv_backward_slicies = get_dependencies(pv_backward_file)

    pv_both_slicies = concat_slicies(pv_forward_slicies, pv_backward_slicies)

    similarities = {}
    for fv in failed_executions_in_failing_products:
        fv_dir = join_path(variants_folder_dir, fv)

        fv_forward_file = get_forward_slicing_file(fv_dir)
        fv_forward_slicies = get_dependencies(fv_forward_file)

        fv_backward_file = get_backward_slicing_file(fv_dir)
        fv_backward_slicies = get_dependencies(fv_backward_file)

        fv_both_slicies = concat_slicies(fv_forward_slicies, fv_backward_slicies)

        for test in failed_executions_in_failing_products[fv]:
            for item in failed_executions_in_failing_products[fv][test]:
                susp_stmt = item["id"]
                similarities = check_dependencies_by_slicing_type(similarities, susp_stmt, fv_forward_slicies,
                                                                  pv_forward_slicies, FORWARD_SLICING_TYPE)
                similarities = check_dependencies_by_slicing_type(similarities, susp_stmt, fv_backward_slicies,
                                                                  pv_backward_slicies, BACKWARD_SLICING_TYPE)
                similarities = check_dependencies_by_slicing_type(similarities, susp_stmt, fv_both_slicies,
                                                                  pv_both_slicies, BOTH_FB_SLICING_TYPE)
    return aggregate_similarity_by_avg(similarities)


def normalization(FIELDS, project_dir, attribute_file, attribute_normalized_file):
    consistent_testing_info_file_path = join_path(project_dir, attribute_file)
    consistent_testing_info_normalized_file = join_path(project_dir, attribute_normalized_file)
    data = pandas.read_csv(consistent_testing_info_file_path)
    variants = data[FIELDS[0]]
    labels = data[FIELDS[1]]
    x = data[FIELDS[2:]].values
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(x)
    data = pandas.DataFrame(x_scaled)
    data.columns = FIELDS[2:]
    data.insert(loc=0, column=FIELDS[1], value=labels)
    data.insert(loc=0, column=FIELDS[0], value=variants)
    data.to_csv(consistent_testing_info_normalized_file)


def calculate_attributes(project_dir, label_file, attribute_temp_file,
                         attribute_normalized_file, FIELDS):
    if not os.path.isfile(join_path(project_dir, label_file)):
        return
    attribute_data = {}
    failing_variants = get_labeled_failing_variants(project_dir, label_file)
    system_stm_ids = get_all_stm_ids(project_dir)
    failed_executions_in_failing_products = get_failings_executions(project_dir, system_stm_ids,
                                                                    failing_variants)

    passed_executions_in_failing_products = get_passing_executions(project_dir, system_stm_ids,
                                                                   failing_variants)
    variants_and_labels = get_variants_and_labels(project_dir, label_file)
    passing_variants_stmts = get_stmts_id_in_passing_variants(project_dir, failing_variants)
    susp_in_passing_variants = {}
    susp_scores_in_system = ranking_suspicious_stmts(project_dir, failing_variants)
    for p_v in passing_variants_stmts:
        attribute_data[p_v] = {}
        susp_in_passing_variants[p_v] = check_suspicious_stmts_in_passing_variants(
            failed_executions_in_failing_products, passing_variants_stmts[p_v])
        var_dir = join_path(join_path(project_dir, "variants"), p_v)
        attribute_data[p_v][LABEL] = variants_and_labels[p_v][LABEL]
        attribute_data[p_v][DDU] = 1 - ddu(var_dir, variants_and_labels[p_v][LABEL])

        not_executed_susp_stmts = check_executed_susp_stmt_vs_susp_stmt_in_passing_variant(
            susp_in_passing_variants[p_v])
        attribute_data[p_v][
            code_coverage] = not_executed_susp_stmts
        passed_executions_in_passing_product = get_passing_executions_in_a_variant(project_dir,
                                                                                   system_stm_ids, p_v)

        attribute_data[p_v][
            incorrectness_verifiability] = check_incorrectness_verifiability(
            failed_executions_in_failing_products, passed_executions_in_passing_product,
            susp_in_passing_variants[p_v], 0.8)

        attribute_data[p_v][
            correctness_reflectability] = check_correctness_reflectability(
            failed_executions_in_failing_products, passed_executions_in_failing_products,
            passed_executions_in_passing_product, susp_in_passing_variants[p_v], 0.8)

        attribute_data[p_v][buggy_statement_containing_possibility] = check_total_susp_scores_in_passing_variant(
            susp_scores_in_system, passing_variants_stmts[p_v])

        dependencies_similarity = check_dependencies(join_path(project_dir, "variants"), p_v,
                                                     failed_executions_in_failing_products)

        attribute_data[p_v][bug_involving_statements] = dependencies_similarity["Both"]
    write_dict_to_file(join_path(project_dir, attribute_temp_file), attribute_data, FIELDS)
    normalization(FIELDS, project_dir, attribute_temp_file, attribute_normalized_file)
    os.remove(join_path(project_dir, attribute_temp_file))


def average_feature_by_label(labels, values, target):
    sum = 0
    count = 0
    for i in range(0, len(labels)):
        if labels[i] == target:
            count += 1
            sum += values[i]

    if count == 0:
        return sum
    return sum / count


import csv
import json

import pandas
from sklearn import preprocessing
from FileManager import *
from consistent_testing_manager.FileName import consistent_testing_info_file, consistent_testing_normalized_info_file

from spectrum_manager.SpectrumReader import get_stm_ids_per_variant, similar_path, \
    get_suspicious_space_consistent_version, get_infor_for_sbfl
from ranking.RankingManager import get_set_of_stms, sbfl_ranking, local_ranking_a_suspicious_list
from spectrum_manager.Spectrum_Expression import OP2

TRUE_PASSING = "TP"
FALSE_PASSING = "FP"
FAILING = "F"
LABELED_FILE_NAME = "variants_testing_label.csv"

VARIANT_NAME = 'VARIANT'
LABEL = 'LABEL'
CREATED_FP = 'FP created from F'
DDU = "consistent_testing_manager"

executed_susp_stmt_vs_susp_stmt_in_passing_variant = "executed_susp_stmt_vs_susp_stmt_in_passing_variant"
not_executed_susp_stmt_vs_susp_stmt_in_passing_variant = "not_executed_susp_stmt_vs_susp_stmt_in_passing_variant"
executed_susp_stmt_vs_susp_stmt_in_a_failed_execution = "executed_susp_stmt_vs_susp_stmt_in_a_failed_execution"
not_executed_susp_stmt_vs_susp_stmt_in_a_failed_execution = "not_executed_susp_stmt_vs_susp_stmt_in_a_failed_execution"
tested_unexpected_behaviors_in_passing_variant = "tested_unexpected_behaviors_in_passing_variant"
confirmed_successes_in_passing_variant = "check_confirmed_successes_in_passing_variant"
total_susp_scores_in_system = "susp_scores_in_system"
total_susp_scores_in_variants = "susp_scores_in_variants"

forward_similarity = "forward_similarity"
backward_similarity = "backward_similarity"
both_forward_and_backward_similarity = "both_forward_and_backward_similarity"


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


def get_labeled_failing_variants(project_dir):
    print(project_dir)
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


def ranking_suspicious_stmts(project_dir, failing_variants):
    search_spaces = get_suspicious_space_consistent_version(project_dir, failing_variants, 0.0, "")

    stm_info_for_sbfl, total_passed_tests, total_failed_tests = get_infor_for_sbfl(
        project_dir, failing_variants,
        "",
        0.0)
    all_stms_f_products_set = get_set_of_stms(search_spaces)
    full_ranked_list = sbfl_ranking(stm_info_for_sbfl, total_failed_tests, total_passed_tests,
                                    all_stms_f_products_set,
                                    [OP2])
    op2_ranked_list = {}
    for (stmt, score, v) in full_ranked_list[OP2]:
        op2_ranked_list[stmt] = score

    return op2_ranked_list


def normalize_score(scores_list):
    min = 10000
    max = -10000
    for (stmt, score, v) in scores_list:
        if score > max:
            max = score
        if score < min:
            min = score
    data = {}
    for (stmt, score, v) in scores_list:
        data[stmt] = (score - min) * (1 / (max - min))
    return data


def get_max_susp_each_stmt_in_variants(project_dir, failing_variants):
    search_spaces = get_suspicious_space_consistent_version(project_dir, failing_variants, 0.0, "")
    suspicious_scores = local_ranking_a_suspicious_list(project_dir, search_spaces, [OP2], "")
    data = {}
    for v in suspicious_scores[OP2]:
        normalized_data = normalize_score(suspicious_scores[OP2][v])
        for stmt in normalized_data:
            if stmt not in data:
                data[stmt] = normalized_data[stmt]
            elif normalized_data[stmt] > data[stmt]:
                data[stmt] = normalized_data[stmt]
    return data


def check_total_susp_scores_in_passing_variant(susp_scores, passing_variant_stmt):
    sum_scores = 0
    for stmt in passing_variant_stmt:
        tmp = passing_variant_stmt[stmt]["id"]
        if tmp in susp_scores:
            sum_scores += susp_scores[tmp]
    return sum_scores


def get_dependencies(slicing_file_dir):
    slicing_file = open(slicing_file_dir, "r")
    slicing_content = slicing_file.readline()
    slicies = json.loads(slicing_content)
    return slicies


def check_similarity_between_two_slicies(pv_slice, fv_slice):
    count = 0
    for s in pv_slice:
        if s in fv_slice:
            count += 1
    return count


def check_dependencies_by_slicing_type(similarities, susp_stmt, fv_slicies, pv_slicies, slicing_type):
    if susp_stmt in fv_slicies:
        if susp_stmt in pv_slicies:
            tmp = check_similarity_between_two_slicies(pv_slicies[susp_stmt], fv_slicies[susp_stmt])
            if susp_stmt not in similarities:
                similarities[susp_stmt] = {}
                similarities[susp_stmt]["Backward"] = 0
                similarities[susp_stmt]["Forward"] = 0
                similarities[susp_stmt]["Both"] = 0

            if len(fv_slicies[susp_stmt]) > 0 and tmp / len(fv_slicies[susp_stmt]) > similarities[susp_stmt][
                slicing_type]:
                similarities[susp_stmt][slicing_type] = tmp / len(fv_slicies[susp_stmt])
    return similarities


def check_overall_dependencies(similarities, fv_forward_slicies, fv_backward_slicies, pv_forward_slicies,
                               pv_backward_slices):
    for stmt in similarities:
        simi_in_fw = 0
        total_slice_length = 0
        if stmt in pv_forward_slicies and stmt in fv_forward_slicies:
            simi_in_fw = check_similarity_between_two_slicies(pv_forward_slicies[stmt], fv_forward_slicies[stmt])
            total_slice_length = len(fv_forward_slicies[stmt])

        simi_in_bw = 0
        if stmt in pv_backward_slices and stmt in fv_backward_slicies:
            simi_in_bw = check_similarity_between_two_slicies(pv_backward_slices[stmt], fv_backward_slicies[stmt])
            total_slice_length += len(fv_backward_slicies[stmt])

        if total_slice_length > 0:
            tmp = (simi_in_bw + simi_in_fw) / total_slice_length
            if tmp > similarities[stmt]["Both"]:
                similarities[stmt]["Both"] = tmp
    return similarities


def aggreate_similarity_by_avg(similarity):
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


def check_dependencies(variants_folder_dir, passing_variant, failed_executions_in_failing_products):
    passing_variant_dir = join_path(variants_folder_dir, passing_variant)
    pv_forward_file = get_forward_slicing_file(passing_variant_dir)
    pv_forward_slicies = get_dependencies(pv_forward_file)

    pv_backward_file = get_backward_slicing_file(passing_variant_dir)
    pv_backward_slicies = get_dependencies(pv_backward_file)

    similarities = {}
    for fv in failed_executions_in_failing_products:
        fv_dir = join_path(variants_folder_dir, fv)

        fv_forward_file = get_forward_slicing_file(fv_dir)
        fv_forward_slicies = get_dependencies(fv_forward_file)

        fv_backward_file = get_backward_slicing_file(fv_dir)
        fv_backward_slicies = get_dependencies(fv_backward_file)

        for test in failed_executions_in_failing_products[fv]:
            for item in failed_executions_in_failing_products[fv][test]:
                susp_stmt = item["id"]
                similarities = check_dependencies_by_slicing_type(similarities, susp_stmt, fv_forward_slicies,
                                                                  pv_forward_slicies, "Forward")
                similarities = check_dependencies_by_slicing_type(similarities, susp_stmt, fv_backward_slicies,
                                                                  pv_backward_slicies, "Backward")
        similarities = check_overall_dependencies(similarities, fv_forward_slicies, fv_backward_slicies,
                                                  pv_forward_slicies, pv_backward_slicies)
    return aggreate_similarity_by_avg(similarities)


def normalization(FIELDS, project_dir):
    consistent_testing_info_file_path = join_path(project_dir, consistent_testing_info_file)
    consistent_testing_info_normalized_file = join_path(project_dir, consistent_testing_normalized_info_file)
    data = pandas.read_csv(consistent_testing_info_file_path)
    variants = data[FIELDS[0]]
    labels = data[FIELDS[1]]
    x = data[FIELDS[2:]].values
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(x)
    data = pandas.DataFrame(x_scaled)
    data.columns = FIELDS[2:]
    data.insert(loc=0, column= FIELDS[1], value=labels)
    data.insert(loc=0, column= FIELDS[0], value=variants)
    data.to_csv(consistent_testing_info_normalized_file)
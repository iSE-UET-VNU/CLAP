from DDU.DDU import ddu
from FileManager import *
from label_data.HelperForLabeledData import *

labels = [FALSE_PASSING, TRUE_PASSING]

if __name__ == "__main__":
    system_dir = "/Users/thu-trangnguyen/Documents/Research/SPL/Debug/1Bug/4wise/"
    mutated_projects = list_dir(system_dir)
    FIELDS = [VARIANT_NAME, LABEL, DDU, executed_susp_stmt_vs_susp_stmt_in_passing_variant,
              not_executed_susp_stmt_vs_susp_stmt_in_passing_variant,
              executed_susp_stmt_vs_susp_stmt_in_a_failed_execution,
              not_executed_susp_stmt_vs_susp_stmt_in_a_failed_execution,
              tested_unexpected_behaviors_in_passing_variant + "_0.5",
              tested_unexpected_behaviors_in_passing_variant + "_0.8",
              tested_unexpected_behaviors_in_passing_variant + "_1.0",
              confirmed_successes_in_passing_variant + "_0.5",
              confirmed_successes_in_passing_variant + "_0.8",
              confirmed_successes_in_passing_variant + "_1.0",
              total_susp_scores_in_system,
              total_susp_scores_in_variants,
              forward_similarity,
              backward_similarity,
              both_forward_and_backward_similarity]
    for project in mutated_projects:
        constant_data = {}
        project_dir = join_path(system_dir, project)
        failing_variants = get_labeled_failing_variants(project_dir)
        system_stm_ids = get_all_stm_ids(project_dir)
        failed_executions_in_failing_products = get_failings_executions(project_dir, system_stm_ids, failing_variants)
        passed_executions_in_failing_products = get_passing_executions(project_dir, system_stm_ids, failing_variants)
        variants_and_labels = get_variants_and_labels(project_dir)
        passing_variants_stmts = get_stmts_id_in_passing_variants(project_dir, failing_variants)
        susp_in_passing_variants= {}
        susp_scores_in_system = ranking_suspicious_stmts(project_dir, failing_variants)
        susp_scores_in_variants = get_max_susp_each_stmt_in_variants(project_dir, failing_variants)
        for p_v in passing_variants_stmts:
            constant_data[p_v] = {}
            susp_in_passing_variants[p_v] = check_suspicious_stmts_in_passing_variants(failed_executions_in_failing_products, passing_variants_stmts[p_v])
            var_dir = join_path(join_path(project_dir, "variants"), p_v)
            constant_data[p_v][LABEL] = variants_and_labels[p_v][LABEL]
            constant_data[p_v][DDU] = 1 - ddu(var_dir, variants_and_labels[p_v][LABEL])
            constant_data[p_v][executed_susp_stmt_vs_susp_stmt_in_passing_variant] = check_executed_susp_stmt_vs_susp_stmt_in_passing_variant(susp_in_passing_variants[p_v])
            constant_data[p_v][not_executed_susp_stmt_vs_susp_stmt_in_passing_variant] = check_not_executed_susp_stmt_vs_susp_stmt_in_passing_variant(susp_in_passing_variants[p_v])
            constant_data[p_v][executed_susp_stmt_vs_susp_stmt_in_a_failed_execution] = check_executed_susp_stmt_vs_susp_stmt_in_a_failed_execution(failed_executions_in_failing_products, susp_in_passing_variants[p_v])
            constant_data[p_v][not_executed_susp_stmt_vs_susp_stmt_in_a_failed_execution] = check_not_executed_susp_stmt_vs_susp_stmt_in_a_failed_execution(failed_executions_in_failing_products, susp_in_passing_variants[p_v])

            passed_executions_in_passing_product = get_passing_executions_in_a_variant(project_dir, system_stm_ids, p_v)
            constant_data[p_v][tested_unexpected_behaviors_in_passing_variant + "_0.5" ] = check_tested_unexpected_behaviors_in_passing_variant(failed_executions_in_failing_products, passed_executions_in_passing_product, susp_in_passing_variants[p_v], 0.5)
            constant_data[p_v][tested_unexpected_behaviors_in_passing_variant + "_0.8" ] = check_tested_unexpected_behaviors_in_passing_variant(failed_executions_in_failing_products, passed_executions_in_passing_product, susp_in_passing_variants[p_v], 0.8)
            constant_data[p_v][tested_unexpected_behaviors_in_passing_variant + "_1.0" ] = check_tested_unexpected_behaviors_in_passing_variant(failed_executions_in_failing_products, passed_executions_in_passing_product, susp_in_passing_variants[p_v], 1.0)

            constant_data[p_v][confirmed_successes_in_passing_variant + "_0.5"] = check_confirmed_successes_in_passing_variant(failed_executions_in_failing_products, passed_executions_in_failing_products, passed_executions_in_passing_product, susp_in_passing_variants[p_v], 0.5)
            constant_data[p_v][confirmed_successes_in_passing_variant + "_0.8"] = check_confirmed_successes_in_passing_variant(failed_executions_in_failing_products, passed_executions_in_failing_products, passed_executions_in_passing_product, susp_in_passing_variants[p_v], 0.8)
            constant_data[p_v][confirmed_successes_in_passing_variant + "_1.0"] = check_confirmed_successes_in_passing_variant(failed_executions_in_failing_products, passed_executions_in_failing_products, passed_executions_in_passing_product, susp_in_passing_variants[p_v], 1.0)

            constant_data[p_v][total_susp_scores_in_system] = check_total_susp_scores_in_passing_variant(susp_scores_in_system, passing_variants_stmts[p_v])
            constant_data[p_v][total_susp_scores_in_variants] = check_total_susp_scores_in_passing_variant(susp_scores_in_variants, passing_variants_stmts[p_v])

            dependencies_similarity = check_dependencies(join_path(project_dir, "variants"), p_v, failed_executions_in_failing_products)
            constant_data[p_v][forward_similarity] = dependencies_similarity["Forward"]
            constant_data[p_v][backward_similarity] = dependencies_similarity["Backward"]
            constant_data[p_v][both_forward_and_backward_similarity] = dependencies_similarity["Both"]
        write_dict_to_file(join_path(project_dir,"consistent_testing_info.csv"), constant_data, FIELDS)

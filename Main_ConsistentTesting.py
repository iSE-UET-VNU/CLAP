from FileManager import *
from label_data.HelperForLabeledData import *

labels = [FALSE_PASSING, ACTUAl_PASSING]

def overlap_in_product():
    system_dir = "/Users/thu-trangnguyen/Documents/Research/SPL/ZipMe/1Bug/2wise/"
    sytem_name = "ZipMe"
    mutated_projects = list_dir(system_dir)
    overlap_mutated_projects = {}
    for project in mutated_projects:
        project_dir = join_path(system_dir, project)
        system_stm_ids = get_all_stm_ids(project_dir)
        failing_variants = get_labeled_failing_variants(project_dir)
        failing_executions = get_failings_executions(project_dir, system_stm_ids, failing_variants)
        passing_variants_stmts = get_stmts_id_in_passing_variants(project_dir, failing_variants)
        variants_and_labels = get_variants_and_labels(project_dir)
        sum  = {}
        count = {}
        for p_variant in passing_variants_stmts:
            max_overlaps = overlap_failed_exection_vs_passing_variant(failing_executions, passing_variants_stmts[p_variant])
            if variants_and_labels[p_variant][LABEL] not in sum:
                sum[variants_and_labels[p_variant][LABEL]] = 0
                count[variants_and_labels[p_variant][LABEL]] = 0
            sum[variants_and_labels[p_variant][LABEL]] += max_overlaps
            count[variants_and_labels[p_variant][LABEL]] += 1

        overlap_mutated_projects[project] = {}
        for l in labels:
            overlap_mutated_projects[project][l] = sum[l]/count[l]

    write_dict_to_file(join_path("/Users/thu-trangnguyen/Documents/Projects/VarCop/experiment_results/Consistent_Testing", sytem_name + "_overlap_portion_p_not_executed_1Bug.csv"),
                       overlap_mutated_projects,
                       ["PROJECT ID", FALSE_PASSING, ACTUAl_PASSING])
# def failed_passed_test_overlap():
#     system_dir = "/Users/thu-trangnguyen/Documents/Research/SPL/ZipMe/1Bug/2wise/"
# sytem_name = "ZipMe"
# mutated_projects = list_dir(system_dir)
# overlap_mutated_projects = {}
# for project in mutated_projects:
#     project_dir = join_path(system_dir, project)
#     failing_variants = get_labeled_failing_variants(project_dir)
#     system_stm_ids = get_all_stm_ids(project_dir)
#     failed_executions_in_failing_products = get_failings_executions(project_dir, system_stm_ids, failing_variants)
#     passed_exections_in_failing_products = get_passing_executions(project_dir, system_stm_ids, failing_variants)
#     variants_and_labels = get_variants_and_labels(project_dir)
#     passing_variants_stmts = get_stmts_id_in_passing_variants(project_dir, failing_variants)
#     passing_variants = []
#     for p_v in passing_variants_stmts:
#         passing_variants.append(p_v)
#     passed_executions_in_passing_products = get_passing_executions(project_dir, system_stm_ids, passing_variants)
#     sum  = {}
#     count_products = {}
#     for p_v in passing_variants_stmts:
#         overlap = overlap_failed_exection_vs_passing_variant(failed_executions_in_failing_products, passing_variants_stmts[p_v])
#         total_overlap_tested = 0
#         count = 0
#         for test in overlap:
#             failed_exection_len = len(failed_executions_in_failing_products[test.split("__")[0]][test.split("__")[1]])
#             overlap_len = len(overlap[test]['Executed']) + len(overlap[test]['Not Executed'])
#             if overlap_len/failed_exection_len > 0.8:
#                 total_overlap_tested += 1
#                 failed_path = failed_executions_in_failing_products[test.split("__")[0]][test.split("__")[1]]
#                 if exist_path(failed_path, passed_executions_in_passing_products[p_v], 0.8):
#                     count += 1
#
#         if(variants_and_labels[p_v][LABEL] not in sum):
#             sum[variants_and_labels[p_v][LABEL]] = 0
#             count_products[variants_and_labels[p_v][LABEL]] = 0
#
#         if total_overlap_tested != 0:
#             sum[variants_and_labels[p_v][LABEL]] += count/total_overlap_tested
#             count_products[variants_and_labels[p_v][LABEL]] += 1
#         else:
#             sum[variants_and_labels[p_v][LABEL]] += 1
#             count_products[variants_and_labels[p_v][LABEL]] += 1
#
#     overlap_mutated_projects[project] = {}
#     for l in labels:
#         overlap_mutated_projects[project][l] = sum[l]/count_products[l]
# write_dict_to_file(join_path("/Users/thu-trangnguyen/Documents/Projects/VarCop/experiment_results/Consistent_Testing", sytem_name + "_failed_passed_tested_overlap.csv"),
#                    overlap_mutated_projects,
#                    ["PROJECT ID", FALSE_PASSING, ACTUAl_PASSING])

if __name__ == "__main__":
    overlap_in_product()
    # system_dir = "/Users/thu-trangnguyen/Documents/Research/SPL/ZipMe/1Bug/2wise/"
    # sytem_name = "ZipMe"
    # mutated_projects = list_dir(system_dir)
    # overlap_mutated_projects = {}
    # for project in mutated_projects:
    #     project_dir = join_path(system_dir, project)
    #     failing_variants = get_labeled_failing_variants(project_dir)
    #     system_stm_ids = get_all_stm_ids(project_dir)
    #     failed_executions_in_failing_products = get_failings_executions(project_dir, system_stm_ids, failing_variants)
    #     passed_exections_in_failing_products = get_passing_executions(project_dir, system_stm_ids, failing_variants)
    #     variants_and_labels = get_variants_and_labels(project_dir)
    #     passing_variants_stmts = get_stmts_id_in_passing_variants(project_dir, failing_variants)
    #     passing_variants = []
    #     for p_v in passing_variants_stmts:
    #         passing_variants.append(p_v)
    #     passed_executions_in_passing_products = get_passing_executions(project_dir, system_stm_ids, passing_variants)
    #     sum  = {}
    #     count_products = {}
    #     for p_v in passing_variants_stmts:
    #         overlap = overlap_failed_exection_vs_passing_variant(failed_executions_in_failing_products, passing_variants_stmts[p_v])
    #         total_overlap_tested = 0
    #         count = 0
    #         considering_failed_variant = []
    #         for test in overlap:
    #             failed_exection_len = len(failed_executions_in_failing_products[test.split("__")[0]][test.split("__")[1]])
    #             overlap_len = len(overlap[test]['Executed']) + len(overlap[test]['Not Executed'])
    #             if overlap_len/failed_exection_len > 0.8:
    #
    #                 if test.split("__")[0] not in considering_failed_variant:
    #                     considering_failed_variant.append(test.split("__")[0])
    #         if variants_and_labels[p_v][LABEL] not in sum:
    #             sum[variants_and_labels[p_v][LABEL]] = 0
    #             count_products[variants_and_labels[p_v][LABEL]] = 0
    #
    #         if len(considering_failed_variant) == 0:
    #            sum[variants_and_labels[p_v][LABEL]] += 1
    #            count_products[variants_and_labels[p_v][LABEL]] += 1
    #
    #         else:
    #             tmp = 0
    #             for v in considering_failed_variant:
    #                 passed_exections_in_v = passed_exections_in_failing_products[v]
    #                 count = 0;
    #                 for test in passed_exections_in_v:
    #                     if exist_path(test, passed_executions_in_passing_products[p_v], 0.8):
    #                         count += 1
    #                 tmp += count/len(passed_exections_in_v)
    #
    #             sum[variants_and_labels[p_v][LABEL]] += tmp/len(considering_failed_variant)
    #             count_products[variants_and_labels[p_v][LABEL]] += 1
    #
    #
    #     overlap_mutated_projects[project] = {}
    #     for l in labels:
    #         overlap_mutated_projects[project][l] = sum[l]/count_products[l]
    # write_dict_to_file(join_path("/Users/thu-trangnguyen/Documents/Projects/VarCop/experiment_results/Consistent_Testing", sytem_name + "_passed_passed_tested_overlap.csv"),
    #                        overlap_mutated_projects,
    #                        ["PROJECT ID", FALSE_PASSING, ACTUAl_PASSING])

from consistent_testing_manager.FileName import classified_all_file
from consistent_testing_manager.LabelData import *

#
# FIELDS = [VARIANT_NAME, LABEL, DDU,
#           not_executed_susp_stmt_vs_susp_stmt_in_passing_variant,
#           executed_susp_stmt_vs_susp_stmt_in_a_failed_execution,
#           not_executed_susp_stmt_vs_susp_stmt_in_a_failed_execution,
#           tested_unexpected_behaviors_in_passing_variant + "_0.8",
#           confirmed_successes_in_passing_variant + "_0.8",
#           total_susp_scores_in_system, both_forward_and_backward_similarity]

FIELDS = [VARIANT_NAME, LABEL, DDU,
          not_executed_susp_stmt_vs_susp_stmt_in_passing_variant,
          executed_susp_stmt_vs_susp_stmt_in_a_failed_execution,
          not_executed_susp_stmt_vs_susp_stmt_in_a_failed_execution,
          tested_unexpected_behaviors_in_passing_variant + "_0.8",
          confirmed_successes_in_passing_variant + "_0.8",
          total_susp_scores_in_variants]



def classify(project_dir, metrics):
    consistent_testing_info_normalized_file_path = join_path(project_dir, consistent_testing_normalized_info_file)
    classified_file = join_path(project_dir, classified_all_file)
    data = pandas.read_csv(consistent_testing_info_normalized_file_path)
    classified_variants = {}
    total_classified_values = 0
    for i in range(0, len(data[VARIANT_NAME])):
        total = 0
        for m in metrics:
            total += data.iloc[i][m]
        classified_variants[data.iloc[i][VARIANT_NAME]] = {}
        classified_variants[data.iloc[i][VARIANT_NAME]][LABEL] = data.iloc[i][LABEL]
        classified_variants[data.iloc[i][VARIANT_NAME]]["Classified_Value"] = total/len(metrics)
        total_classified_values += total/len(metrics)

    average_value = total_classified_values/len(classified_variants)
    for variant in classified_variants:
        if classified_variants[variant]["Classified_Value"] >= average_value:
            classified_variants[variant]["Classified"] = "FP"
        else:
            classified_variants[variant]["Classified"] = "TP"
    write_dict_to_file(classified_file, classified_variants, [VARIANT_NAME, LABEL, "Classified_Value", "Classified"])


if __name__ == "__main__":
    system_dir = "/Users/thu-trangnguyen/Documents/Research/SPL/ZipMe/1Bug/2wise/"
    mutated_projects = list_dir(system_dir)
    average_ddu = {}
    #sytem_name = "ZipMe"
    for project in mutated_projects:
        print(project)
        project_dir = join_path(system_dir, project)
        #normalization(project_dir)
        classify(project_dir, FIELDS[2:])

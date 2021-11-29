import csv

from FileManager import list_dir, join_path
import pandas

from label_data.LabelData import *
from sklearn import preprocessing

# FIELDS = [VARIANT_NAME, LABEL, DDU, executed_susp_stmt_vs_susp_stmt_in_passing_variant,
#           not_executed_susp_stmt_vs_susp_stmt_in_passing_variant,
#           executed_susp_stmt_vs_susp_stmt_in_a_failed_execution,
#           not_executed_susp_stmt_vs_susp_stmt_in_a_failed_execution,
#           tested_unexpected_behaviors_in_passing_variant + "_0.5",
#           tested_unexpected_behaviors_in_passing_variant + "_0.8",
#           tested_unexpected_behaviors_in_passing_variant + "_1.0",
#           confirmed_successes_in_passing_variant + "_0.5",
#           confirmed_successes_in_passing_variant + "_0.8",
#           confirmed_successes_in_passing_variant + "_1.0",
#           total_susp_scores_in_system,
#           total_susp_scores_in_variants,
#           forward_similarity,
#           backward_similarity,
#           both_forward_and_backward_similarity]

FIELDS = [VARIANT_NAME, LABEL, DDU,
          not_executed_susp_stmt_vs_susp_stmt_in_passing_variant,
          executed_susp_stmt_vs_susp_stmt_in_a_failed_execution,
          not_executed_susp_stmt_vs_susp_stmt_in_a_failed_execution,
          tested_unexpected_behaviors_in_passing_variant + "_0.8",
          confirmed_successes_in_passing_variant + "_0.8",
          total_susp_scores_in_system, both_forward_and_backward_similarity]

# FIELDS = [VARIANT_NAME, LABEL, DDU,
#           not_executed_susp_stmt_vs_susp_stmt_in_passing_variant,
#           executed_susp_stmt_vs_susp_stmt_in_a_failed_execution,
#           not_executed_susp_stmt_vs_susp_stmt_in_a_failed_execution,
#           tested_unexpected_behaviors_in_passing_variant + "_0.8",
#           confirmed_successes_in_passing_variant + "_0.8",
#           total_susp_scores_in_variants]




def normalization(project_dir):
    consistent_testing_info_file = join_path(project_dir, "consistent_testing_info.csv")
    consistent_testing_info_normalized_file = join_path(project_dir, "consistent_testing_info_normalized.csv")
    data = pandas.read_csv(consistent_testing_info_file)
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


def classify(project_dir, metrics):
    consistent_testing_info_normalized_file = join_path(project_dir, "consistent_testing_info_normalized.csv")
    classified_file = join_path(project_dir, "classification_info_sups_in_variants_dependencies.csv")
    #classified_file = join_path(project_dir, "classification_info_sups_in_variants.csv")
    data = pandas.read_csv(consistent_testing_info_normalized_file)
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

import pandas

from FileManager import list_dir, join_path
from label_data.LabelData import *
import json

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


def calculate_average(labels, values, target):
    sum = 0
    count = 0
    for i in range(0, len(labels)):
        if labels[i] == target:
            count += 1
            sum += values[i]

    if count == 0:
        return sum
    return sum / count


def aggreate_result(system_dir, mutated_projects):
    average_values = {TRUE_PASSING: {}, FALSE_PASSING: {}}
    for f in FIELDS[2:]:
        average_values[TRUE_PASSING][f] = 0
        average_values[FALSE_PASSING][f] = 0

    for project in mutated_projects:
        project_dir = join_path(system_dir, project)
        consistent_testing_info_normalized_file = join_path(project_dir, "consistent_testing_info_normalized.csv")
        data = pandas.read_csv(consistent_testing_info_normalized_file)
        for f in FIELDS[2:]:
            average_values[TRUE_PASSING][f] += calculate_average(data[LABEL], data[f], TRUE_PASSING)
            average_values[FALSE_PASSING][f] += calculate_average(data[LABEL], data[f], FALSE_PASSING)

    for f in FIELDS[2:]:
        average_values[TRUE_PASSING][f] /= len(mutated_projects)
        average_values[FALSE_PASSING][f] /= len(mutated_projects)

    for l in average_values:
        print(l)
        for item in average_values[l]:
            print(item, ":   ", round(average_values[l][item], 2))


def classification_accuracy(system_dir, mutated_projects, file_name):
    with open('accuracy.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(["MUTATED_PROJECT", "TP_ACCURACY", "FP_ACCURACY", "ACCURACY"])
        total_TP_accuracy = 0
        total_FP_accuracy = 0
        total_accuracy = 0
        for project in mutated_projects:
            project_dir = join_path(system_dir, project)
            classify_file = join_path(project_dir, file_name)

            with open(classify_file) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                TP_count = 0
                FP_count = 0
                TP_correct = 0
                FP_correct = 0
                for row in csv_reader:
                    if row[1] == TRUE_PASSING:
                        TP_count += 1
                        if row[1] == row[-1]:
                            TP_correct += 1
                    elif row[1] == FALSE_PASSING:
                        FP_count += 1
                        if row[1] == row[-1]:
                            FP_correct += 1

                TP_accuracy = TP_correct / TP_count
                FP_accuracy = FP_correct / FP_count
                accuracy = (TP_correct + FP_correct) / (TP_count + FP_count)
                writer.writerow([project, TP_accuracy, FP_accuracy, accuracy])
                total_TP_accuracy += TP_accuracy
                total_FP_accuracy += FP_accuracy
                total_accuracy += accuracy
        writer.writerow(
            ["Average", total_TP_accuracy / len(mutated_projects), total_FP_accuracy / len(mutated_projects),
             total_accuracy / len(mutated_projects)])


def confusion_matrix(system_dir, mutated_projects, classified_file):
    matrix = {"TP_correct":0, "TP_incorrect": 0, "FP_correct":0, "FP_incorrect": 0}

    for project in mutated_projects:
        project_dir = join_path(system_dir, project)
        classified_file_dir = join_path(project_dir, classified_file)
        data = pandas.read_csv(classified_file_dir)
        for i in range(0, len(data[LABEL])):
            if data[LABEL][i] == TRUE_PASSING:
                if data["Classified"][i] == TRUE_PASSING:
                    matrix["TP_correct"] += 1
                else:
                    matrix["TP_incorrect"] += 1
            else:
                if data["Classified"][i] == FALSE_PASSING:
                    matrix["FP_correct"] += 1
                else:
                    matrix["FP_incorrect"] += 1
    print(matrix)


if __name__ == "__main__":
    system_dir = "/Users/thu-trangnguyen/Documents/Research/SPL/Email/2Bug/4wise/"

    mutated_projects = list_dir(system_dir)
    # aggreate_result(system_dir, mutated_projects)
    # classification_accuracy(system_dir, mutated_projects, "classification_info_sups_in_variants_dependencies.csv")
    confusion_matrix(system_dir, mutated_projects, "classification_info_sups_in_variants_dependencies.csv")

import pandas
from sklearn import svm
from sklearn import metrics
from xlsxwriter import Workbook

from consistent_testing_manager.FPMatricsCaculation import *
import numpy as np
from consistent_testing_manager.FileName import *
from consistent_testing_manager.LabelData import label_data, do_label_statistics

CLASSIFY_FEATURES = [DDU, not_executed_susp_stmt_vs_susp_stmt_in_passing_variant,
                     executed_susp_stmt_vs_susp_stmt_in_a_failed_execution,
                     not_executed_susp_stmt_vs_susp_stmt_in_a_failed_execution,
                     tested_unexpected_behaviors_in_passing_variant_80,
                     confirmed_successes_in_passing_variant_80,
                     total_susp_scores_in_system,
                     both_forward_and_backward_similarity]

FIELDS = [VARIANT_NAME, LABEL, DDU, executed_susp_stmt_vs_susp_stmt_in_passing_variant,
          not_executed_susp_stmt_vs_susp_stmt_in_passing_variant,
          executed_susp_stmt_vs_susp_stmt_in_a_failed_execution,
          not_executed_susp_stmt_vs_susp_stmt_in_a_failed_execution,
          tested_unexpected_behaviors_in_passing_variant_50,
          tested_unexpected_behaviors_in_passing_variant_80,
          tested_unexpected_behaviors_in_passing_variant_100,
          confirmed_successes_in_passing_variant_50,
          confirmed_successes_in_passing_variant_80,
          confirmed_successes_in_passing_variant_100,
          total_susp_scores_in_system,
          total_susp_scores_in_variants, forward_similarity, backward_similarity, both_forward_and_backward_similarity]


def labeled_cases_count(system_dir):
    mutated_projects = list_dir(system_dir)
    total_labeled_cases = 0
    for project in mutated_projects:
        project_dir = join_path(system_dir, project)
        if os.path.isfile(join_path(project_dir, variants_testing_label_file)):
            total_labeled_cases += 1
    return total_labeled_cases


def load_all_data(logfile, training_systems, testing_systems, system_ratio, variant_ratio=0):
    all_systems = []
    for s in training_systems:
        all_systems.append(s)
    for s in testing_systems:
        all_systems.append(s)

    train_temp = []
    test_temp = []
    test_sample = {}
    training_system = 0
    testing_system = 0
    training_tp = 0
    training_fp = 0
    testing_tp = 0
    testing_fp = 0
    for system in all_systems:
        count = 0
        test_sample[system] = []
        total_labeled_cases = labeled_cases_count(system)
        mutated_projects = list_dir(system)
        for project in mutated_projects:
            project_dir = join_path(system, project)
            consistent_testing_info_normalized_file_path = join_path(project_dir,
                                                                     consistent_testing_normalized_info_file)
            if not os.path.isfile(consistent_testing_info_normalized_file_path):
                continue
            df = pandas.read_csv(consistent_testing_info_normalized_file_path)
            if system in training_systems or count < system_ratio * total_labeled_cases:
                if variant_ratio == 0:
                    train_temp.append(df)
                else:
                    num_train_items = int(variant_ratio * df.shape[0])
                    df1 = df.iloc[:num_train_items, :]
                    df2 = df.iloc[num_train_items + 1:, :]
                    train_temp.append(df1)
                    test_temp.append(df2)
                    test_sample[system].append(project)
                    testing_system += 1
                count += 1
                training_system += 1
            else:
                if variant_ratio == 0:
                    test_temp.append(df)
                else:
                    num_train_items = int(variant_ratio * df.shape[0])
                    df1 = df.iloc[:num_train_items, :]
                    df2 = df.iloc[num_train_items + 1:, :]
                    train_temp.append(df1)
                    test_temp.append(df2)
                    training_system += 1
                test_sample[system].append(project)
                testing_system += 1

    train_result = pandas.concat(train_temp)
    train_data = train_result[CLASSIFY_FEATURES].to_numpy()
    train_target = train_result[LABEL].to_numpy()
    training_tp += np.count_nonzero(train_target == TRUE_PASSING)
    training_fp += np.count_nonzero(train_target == FALSE_PASSING)
    train_target[train_target == TRUE_PASSING] = 0
    train_target[train_target == FALSE_PASSING] = 1

    test_result = pandas.concat(test_temp)
    test_data = test_result[CLASSIFY_FEATURES].to_numpy()
    test_target = test_result[LABEL].to_numpy()
    testing_tp += np.count_nonzero(test_target == TRUE_PASSING)
    testing_fp += np.count_nonzero(test_target == FALSE_PASSING)
    test_target[test_target == TRUE_PASSING] = 0
    test_target[test_target == FALSE_PASSING] = 1

    logfile.write("training system: " + str(training_system) + "\n")
    logfile.write("testing system: " + str(testing_system) + "\n")
    logfile.write("Training tp: " + str(training_tp) + "\n")
    logfile.write("Training fp: " + str(training_fp) + "\n")
    logfile.write("Testing tp: " + str(testing_tp) + "\n")
    logfile.write("Testing fp: " + str(testing_fp) + "\n")
    logfile.write("-------------\n")
    return train_data, test_data, train_target.astype('int'), test_target.astype('int'), test_sample


def write_classified_result(y_pred, test_samples, variant_ratio, file_name):
    predict_index = 0
    for system in test_samples:
        testing_projects = test_samples[system]
        if len(testing_projects) == 0:
            continue
        for project in testing_projects:
            data = {}
            project_dir = join_path(system, project)
            consistent_testing_info_normalized_file = join_path(project_dir, "consistent_testing_info_normalized.csv")
            df = pandas.read_csv(consistent_testing_info_normalized_file)
            if variant_ratio == 0:
                variants = df[VARIANT_NAME]
                labels = df[LABEL]
                label_index = 0
            else:
                num_train_items = int(variant_ratio * df.shape[0])
                variants = df.iloc[num_train_items + 1:, :][VARIANT_NAME]
                labels = df.iloc[num_train_items + 1:, :][LABEL]
                label_index = num_train_items + 1

            for v in variants:
                if y_pred[predict_index] == 0:
                    data[v] = {LABEL: labels[label_index], "Classified": TRUE_PASSING}
                else:
                    data[v] = {LABEL: labels[label_index], "Classified": FALSE_PASSING}
                label_index += 1
                predict_index += 1
            classified_file = join_path(project_dir, file_name)
            write_dict_to_file(classified_file, data, [VARIANT_NAME, LABEL, "Classified"])


def overall_performance_measurement(y_test, y_pred, logfile):
    TP_count = 0
    TP_correct = 0
    FP_count = 0
    FP_correct = 0
    predict_index = 0
    for l in y_test:
        if l == 1:
            FP_count += 1
            if y_pred[predict_index] == 1:
                FP_correct += 1
        else:
            TP_count += 1
            if y_pred[predict_index] == 0:
                TP_correct += 1
        predict_index += 1
    logfile.write("tp_count: " + str(TP_count) + "\n")
    logfile.write("tp_correct: " + str(TP_correct) + "\n")
    logfile.write("fp_count: " + str(FP_count) + "\n")
    logfile.write("fp_correct: " + str(FP_correct) + "\n")
    logfile.write("tp_precision:" + str(TP_correct / (TP_correct + FP_count - FP_correct)) + "\n")
    logfile.write("fp_precision: " + str(FP_correct / (FP_correct + TP_count - TP_correct)) + "\n")
    logfile.write("tp_recall: " + str(TP_correct / TP_count) + "\n")
    logfile.write("fp_recall: " + str(FP_correct / FP_count) + "\n")
    logfile.write("-------------\n")


def performance_in_each_projects(testing_systems, classified_file, logfile):
    for system in testing_systems:
        TP_correct = 0
        FP_correct = 0
        FP_count = 0
        TP_count = 0
        logfile.write(system + "\n")
        for project in testing_systems[system]:
            classified_file_path = join_path(join_path(system, project), classified_file)
            with open(classified_file_path) as file:
                csvFile = csv.reader(file)
                for line in csvFile:
                    if line[1] == TRUE_PASSING:
                        TP_count += 1
                        if line[2] == TRUE_PASSING:
                            TP_correct += 1
                    else:
                        FP_count += 1
                        if line[2] == FALSE_PASSING:
                            FP_correct += 1
        if TP_count == 0 or FP_count == 0:
            break
        logfile.write("tp_precision: " + str(TP_correct / (TP_correct + FP_count - FP_correct)) + "\n")
        logfile.write("fp_precision: " + str(FP_correct / (FP_correct + TP_count - TP_correct)) + "\n")
        logfile.write("tp_recall: " + str(TP_correct / TP_count) + "\n")
        logfile.write("fp_recall: " + str(FP_correct / (FP_count)) + "\n")
        logfile.write("accuracy: " + str((TP_correct + FP_correct) / (TP_count + FP_count)) + "\n")
        logfile.write("-------------\n")


def classify(logfile, classified_result_file, training_systems, testing_system, system_ratio, variant_ratio=0):
    X_train, X_test, y_train, y_test, test_samples = load_all_data(logfile, training_systems, testing_system,
                                                                   system_ratio, variant_ratio)
    clf = svm.SVC(kernel='linear')
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    logfile.write("Accuracy: " + str(metrics.accuracy_score(y_test, y_pred)) + "\n")
    overall_performance_measurement(y_test, y_pred, logfile)

    write_classified_result(y_pred, test_samples, 0, classified_result_file)
    performance_in_each_projects(test_samples, classified_result_file, logfile)


def classify_all_cases(system_paths):
    logfile = open("statistics/classified_all_cases.log", "w")
    testing_systems = []
    for s in system_paths:
        for b in system_paths[s]:
            testing_systems.append(system_paths[s][b])

    classify(logfile, classified_all_cases_file, [], testing_systems, 0.8, 0.0)
    logfile.close()


def classify_single_bug_cases(system_paths):
    testing_systems = []
    for s in system_paths:
        if "1Bug" in system_paths[s]:
            testing_systems.append(system_paths[s]["1Bug"])
    logfile = open("statistics/classified_single_bug_cases.log", "w")
    classify(logfile, classified_single_bug_file, [], testing_systems, 0.8, 0.0)
    logfile.close()


def classify_by_variants(system_paths):
    logfile = open("statistics/classified_by_variants.log", "w")
    testing_systems = []
    for s in system_paths:
        for b in system_paths[s]:
            testing_systems.append(system_paths[s][b])

    X_train, X_test, y_train, y_test, test_samples = load_all_data(logfile, [], testing_systems,
                                                                   0.0, 0.8)
    clf = svm.SVC(kernel='linear')
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    logfile.write("Accuracy: " + str(metrics.accuracy_score(y_test, y_pred)) + "\n")
    overall_performance_measurement(y_test, y_pred, logfile)
    logfile.close()


def classify_by_systems(system_paths):
    logfile = open("statistics/classified_by_systems.log", "w")
    for s1 in system_paths:
        logfile.write("testing system: " + s1 + "\n")
        training_set = []
        testing_set = []
        for s2 in system_paths:
            for bug in system_paths[s2]:
                if s1 == s2:
                    testing_set.append(system_paths[s2][bug])
                else:
                    training_set.append(system_paths[s2][bug])

        logfile.write("---------\n")
        classify(logfile, classified_by_systems_file, training_set, testing_set, 0.0, 0.0)
    logfile.close()


def classify_by_only_a_system(system_paths):
    logfile = open("statistics/classified_by_only_a_system.log", "w")
    for s in system_paths:
        logfile.write("testing system: " + s + "\n")
        testing_set = []
        for bug in system_paths[s]:
            testing_set.append(system_paths[s][bug])

        logfile.write("---------\n")
        classify(logfile, classified_by_systems_file, [], testing_set, 0.8, 0.0)
    logfile.close()
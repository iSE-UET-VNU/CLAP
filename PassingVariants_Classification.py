import pandas
from sklearn import svm
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn import metrics
from xlsxwriter import Workbook
import matplotlib.pyplot as plt

from consistent_testing_manager.FPMatricsCaculation import *
import numpy as np
from consistent_testing_manager.FileName import *
from consistent_testing_manager.LabelData import label_data, do_label_statistics, label_training_data, \
    label_testing_data
import random

CLASSIFY_FEATURES = [DDU, not_executed_susp_stmt_vs_in_passing_variant,
                     both_forward_and_backward_similarity,
                     total_susp_scores_in_system,
                     tested_unexpected_behaviors_in_passing_variant_80,
                     confirmed_successes_in_passing_variant_80]

FIELDS = [VARIANT_NAME, LABEL, DDU, executed_susp_stmt_in_passing_variant,
          not_executed_susp_stmt_vs_in_passing_variant,

          tested_unexpected_behaviors_in_passing_variant_80,

          confirmed_successes_in_passing_variant_80,

          total_susp_scores_in_system,
          both_forward_and_backward_similarity]


def labeled_cases_count(system_dir):
    mutated_projects = list_dir(system_dir)
    total_labeled_cases = 0
    for project in mutated_projects:
        project_dir = join_path(system_dir, project)
        if os.path.isfile(join_path(project_dir, label_for_training)):
            total_labeled_cases += 1
    return total_labeled_cases


def load_all_data_cross_version(logfile, all_systems, features):
    buggy_versions = []

    for system in all_systems:
        mutated_projects = list_dir(system)
        for project in mutated_projects:
            project_dir = join_path(system, project)
            buggy_versions.append(project_dir)
    random.shuffle(buggy_versions)
    set1 = []
    set2 = []
    set3 = []
    set4 = []
    set5 = []
    for i in range(0, len(buggy_versions)):
        if i <= 0.2 * len(buggy_versions):
            set1.append(buggy_versions[i])
        elif i <= 0.4 * len(buggy_versions):
            set2.append(buggy_versions[i])
        elif i <= 0.6 * len(buggy_versions):
            set3.append(buggy_versions[i])
        elif i <= 0.8 * len(buggy_versions):
            set4.append(buggy_versions[i])
        else:
            set5.append(buggy_versions[i])
    training_set = set1 + set2 + set3 + set4

    testing_set = set5
    train_temp = []
    test_temp = []
    test_sample = {}
    training_system = 0
    testing_system = 0
    training_tp = 0
    training_fp = 0
    testing_tp = 0
    testing_fp = 0

    for project in buggy_versions:
        project_dir = join_path(system, project)

        if project in training_set:
            consistent_testing_info_normalized_file_path = join_path(project_dir,
                                                                     consistent_testing_normalized_info_for_training)
            if not os.path.isfile(consistent_testing_info_normalized_file_path):
                continue
            df = pandas.read_csv(consistent_testing_info_normalized_file_path)
            train_temp.append(df)
            training_system += 1
        else:
            consistent_testing_info_normalized_file_path = join_path(project_dir,
                                                                     consistent_testing_normalized_info_for_testing)
            if not os.path.isfile(consistent_testing_info_normalized_file_path):
                continue
            df = pandas.read_csv(consistent_testing_info_normalized_file_path)
            test_temp.append(df)
            testing_system += 1

    train_result = pandas.concat(train_temp)
    train_data = train_result[features].to_numpy()
    train_target = train_result[LABEL].to_numpy()
    training_tp += np.count_nonzero(train_target == TRUE_PASSING)
    training_fp += np.count_nonzero(train_target == FALSE_PASSING)
    train_target[train_target == TRUE_PASSING] = 0
    train_target[train_target == FALSE_PASSING] = 1

    test_result = pandas.concat(test_temp)
    test_data = test_result[features].to_numpy()
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


def load_all_for_system_edition(logfile, training_systems, testing_systems, features):
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
        test_sample[system] = []
        mutated_projects = list_dir(system)
        for project in mutated_projects:
            project_dir = join_path(system, project)

            if system in training_systems:
                consistent_testing_normalized_info_for_training_path = join_path(project_dir,
                                                                         consistent_testing_normalized_info_for_training)
                if os.path.isfile(consistent_testing_normalized_info_for_training_path):
                    df = pandas.read_csv(consistent_testing_normalized_info_for_training_path)
                    train_temp.append(df)
                    training_system += 1
            else:
                consistent_testing_normalized_info_for_testing_path = join_path(project_dir,
                                                                         consistent_testing_normalized_info_for_testing)
                if os.path.isfile(consistent_testing_normalized_info_for_testing_path):
                    df = pandas.read_csv(consistent_testing_normalized_info_for_testing_path)
                    test_temp.append(df)
                    test_sample[system].append(project)
                    testing_system += 1
    train_result = pandas.concat(train_temp)
    train_data = train_result[features].to_numpy()
    train_target = train_result[LABEL].to_numpy()
    training_tp += np.count_nonzero(train_target == TRUE_PASSING)
    training_fp += np.count_nonzero(train_target == FALSE_PASSING)
    train_target[train_target == TRUE_PASSING] = 0
    train_target[train_target == FALSE_PASSING] = 1

    test_result = pandas.concat(test_temp)
    test_data = test_result[features].to_numpy()
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


def write_classified_result(y_pred, test_samples, file_name):
    predict_index = 0
    for system in test_samples:
        testing_projects = test_samples[system]
        if len(testing_projects) == 0:
            continue
        for project in testing_projects:
            data = {}
            project_dir = join_path(system, project)
            consistent_testing_info_normalized_file = join_path(project_dir, consistent_testing_normalized_info_for_testing)
            df = pandas.read_csv(consistent_testing_info_normalized_file)

            variants = df[VARIANT_NAME]
            labels = df[LABEL]
            label_index = 0

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
        logfile.write("fp_recall: " + str(FP_correct / FP_count) + "\n")
        logfile.write("accuracy: " + str((TP_correct + FP_correct) / (TP_count + FP_count)) + "\n")
        logfile.write("-------------\n")


def classify_by_svm(logfile, classified_result_file, X_train, X_test, y_train, y_test, test_samples,
                    classified_by_variant):
    start = time.time()
    clf = svm.SVC(kernel='linear')
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)

    logfile.write("Accuracy: " + str(metrics.accuracy_score(y_test, y_pred)) + "\n")
    overall_performance_measurement(y_test, y_pred, logfile)
    if not classified_by_variant:
        write_classified_result(y_pred, test_samples, classified_result_file)
    end = time.time()
    logfile.write("run_time:" + str(end - start) + "\n")
    # if not classified_by_variant:
    #     performance_in_each_projects(test_samples, classified_result_file, logfile)


def classify_by_knn(logfile, classified_result_file, X_train, X_test, y_train, y_test, test_samples):
    start = time.time()
    model = KNeighborsClassifier(n_neighbors=3)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    logfile.write("Accuracy: " + str(metrics.accuracy_score(y_test, y_pred)) + "\n")
    overall_performance_measurement(y_test, y_pred, logfile)
    # if not classified_by_variant:
    # write_classified_result(y_pred, test_samples, 0, classified_result_file)
    end = time.time()
    logfile.write("run_time:" + str(end - start) + "\n")


def classify_by_naive_bayes(logfile, classified_result_file, X_train, X_test, y_train, y_test, test_samples):
    start = time.time()
    model = GaussianNB()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    logfile.write("Accuracy: " + str(metrics.accuracy_score(y_test, y_pred)) + "\n")
    overall_performance_measurement(y_test, y_pred, logfile)
    end = time.time()
    logfile.write("run_time:" + str(end - start) + "\n")


def classify_by_logistic_regression(logfile, classified_result_file, X_train, X_test, y_train, y_test, test_samples):
    start = time.time()
    model = LogisticRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    logfile.write("Accuracy: " + str(metrics.accuracy_score(y_test, y_pred)) + "\n")
    overall_performance_measurement(y_test, y_pred, logfile)
    end = time.time()
    logfile.write("run_time:" + str(end - start) + "\n")


def classify_by_decisiontree(logfile, classified_result_file, X_train, X_test, y_train, y_test, test_samples):
    start = time.time()
    model = DecisionTreeClassifier(max_depth=10, random_state=101, max_features=None, min_samples_leaf=15)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    logfile.write("Accuracy: " + str(metrics.accuracy_score(y_test, y_pred)) + "\n")
    overall_performance_measurement(y_test, y_pred, logfile)
    end = time.time()
    logfile.write("run_time:" + str(end - start) + "\n")


def classify_by_different_classifiers(logfile, mode, classified_result_file, X_train, X_test, y_train, y_test,
                                      test_samples, classified_by_variant=False):
    logfile.write(mode + " - SVM\n")
    classify_by_svm(logfile, classified_result_file, X_train, X_test, y_train, y_test, test_samples,
                    classified_by_variant)
    logfile.write("-----------------\n")
    logfile.write(mode + " - KNN\n")
    classify_by_knn(logfile, classified_result_file, X_train, X_test, y_train, y_test, test_samples)
    logfile.write("-----------------\n")
    logfile.write(mode + " - Naive bayes\n")
    classify_by_naive_bayes(logfile, classified_result_file, X_train, X_test, y_train, y_test, test_samples)
    logfile.write("-----------------\n")
    logfile.write(mode + " - Logistic regression\n")
    classify_by_logistic_regression(logfile, classified_result_file, X_train, X_test, y_train, y_test, test_samples)
    logfile.write("-----------------\n")
    logfile.write(mode + " - Decision tree\n")
    classify_by_decisiontree(logfile, classified_result_file, X_train, X_test, y_train, y_test, test_samples)


# def classify_all_cases_turn_off_testing(logfile, training_systems, testing_systems):
#     features = [not_executed_susp_stmt_vs_in_passing_variant, DDU]
#
#     X_train, X_test, y_train, y_test, test_samples = load_all_data(logfile, training_systems, testing_systems, features,
#                                                                    system_ratio=0.8, variant_ratio=0.0)
#     classify_by_different_classifiers(logfile, "turn off testing features", classified_testing_file, X_train, X_test,
#                                       y_train, y_test, test_samples)
#
#
# def classify_all_cases_turn_off_programs(logfile, training_systems, testing_systems):
#     features = [both_forward_and_backward_similarity, total_susp_scores_in_system]
#
#     X_train, X_test, y_train, y_test, test_samples = load_all_data(logfile, training_systems, testing_systems, features,
#                                                                    system_ratio=0.8, variant_ratio=0.0)
#     classify_by_different_classifiers(logfile, "turn off programs features", classified_testing_file, X_train, X_test,
#                                       y_train, y_test, test_samples)
#
#
# def classify_all_cases_turn_off_tests_and_programs(logfile, training_systems, testing_systems):
#     features = [tested_unexpected_behaviors_in_passing_variant_80,
#                 confirmed_successes_in_passing_variant_80]
#     X_train, X_test, y_train, y_test, test_samples = load_all_data(logfile, training_systems, testing_systems, features,
#                                                                    system_ratio=0.8, variant_ratio=0.0)
#     classify_by_different_classifiers(logfile, "turn off testing and program features", classified_testing_file,
#                                       X_train, X_test, y_train, y_test, test_samples)


def chart_drawing(statistic_data):
    new_data = {"TP": {}, "FP": {}}
    new_data["TP"]["[0-0.1)"] = statistic_data[0.0]["TP"]
    new_data["FP"]["[0-0.1)"] = statistic_data[0.0]["FP"]

    new_data["TP"]["[0.1-0.2)"] = statistic_data[0.1]["TP"]
    new_data["FP"]["[0.1-0.2)"] = statistic_data[0.1]["FP"]

    new_data["TP"]["[0.2-0.3)"] = statistic_data[0.2]["TP"]
    new_data["FP"]["[0.2-0.3)"] = statistic_data[0.2]["FP"]

    new_data["TP"]["[0.3-0.4)"] = statistic_data[0.3]["TP"]
    new_data["FP"]["[0.3-0.4)"] = statistic_data[0.3]["FP"]

    new_data["TP"]["[0.4-0.5)"] = statistic_data[0.4]["TP"]
    new_data["FP"]["[0.4-0.5)"] = statistic_data[0.4]["FP"]

    new_data["TP"]["[0.5-0.6)"] = statistic_data[0.5]["TP"]
    new_data["FP"]["[0.5-0.6)"] = statistic_data[0.5]["FP"]

    new_data["TP"]["[0.6-0.7)"] = statistic_data[0.6]["TP"]
    new_data["FP"]["[0.6-0.7)"] = statistic_data[0.6]["FP"]

    new_data["TP"]["[0.7-0.8)"] = statistic_data[0.7]["TP"]
    new_data["FP"]["[0.7-0.8)"] = statistic_data[0.7]["FP"]

    new_data["TP"]["[0.8-0.9)"] = statistic_data[0.8]["TP"]
    new_data["FP"]["[0.8-0.9)"] = statistic_data[0.8]["FP"]

    new_data["TP"]["[0.9-1.0]"] = statistic_data[0.9]["TP"] + statistic_data[1.0]["TP"]
    new_data["FP"]["[0.9-1.0]"] = statistic_data[0.9]["FP"] + statistic_data[1.0]["FP"]
    df = pandas.DataFrame.from_dict(new_data)
    df.to_csv("data.csv")


# def statistic_data_for_papers(system_paths):
#     values = set()
#     data = {}
#     for item in FIELDS[2:]:
#         data[item] = {0.0: {"TP": 0, "FP": 0},
#                       0.1: {"TP": 0, "FP": 0},
#                       0.2: {"TP": 0, "FP": 0},
#                       0.3: {"TP": 0, "FP": 0},
#                       0.4: {"TP": 0, "FP": 0},
#                       0.5: {"TP": 0, "FP": 0},
#                       0.6: {"TP": 0, "FP": 0},
#                       0.7: {"TP": 0, "FP": 0},
#                       0.8: {"TP": 0, "FP": 0},
#                       0.9: {"TP": 0, "FP": 0},
#                       1.0: {"TP": 0, "FP": 0}}
#     for s in system_paths:
#         for b in system_paths[s]:
#             mutated_projects = os.listdir(system_paths[s][b])
#             total_projects = labeled_cases_count(system_paths[s][b])
#             count = 0
#             for project in mutated_projects:
#                 print(project)
#                 project_dir = join_path(system_paths[s][b], project)
#                 if ".DS" not in project and os.path.isfile(join_path(project_dir, variants_testing_label_file)):
#                     count += 1
#                     feature_file = join_path(project_dir, consistent_testing_normalized_info_file)
#                     df = pandas.read_csv(feature_file)
#                     for item in FIELDS[2:3]:
#                         for i in range(0, len(df[item])):
#                             v = df[item][i].round(1)
#                             data[item][v][df[LABEL][i]] += 1
#                     if count > 0.8 * total_projects:
#                         break
#     print(values)
#     return data


# def draw_plot(system_paths, y_title, feature):
#     logfile = open("statistics/drawing.log", "w")
#     testing_systems = []
#     for s in system_paths:
#         for b in system_paths[s]:
#             testing_systems.append(system_paths[s][b])
#     training_systems = []
#     X_train, X_test, y_train, y_test, test_samples = load_all_data(logfile, training_systems, testing_systems,
#                                                                    feature,
#                                                                    system_ratio=0.5, variant_ratio=0.0)
#
#     tp_data = []
#     fp_data = []
#     for i in range(0, len(y_train)):
#         if y_train[i] == 1:
#             fp_data.append(X_train[i][0])
#         else:
#             tp_data.append(X_train[i][0])
#
#     if len(tp_data) > len(fp_data):
#         data = {'TP_product': tp_data[0:len(fp_data)], "FP_product": fp_data}
#     else:
#         data = {'TP_product': tp_data, "FP_product": fp_data[:len(tp_data)]}
#
#     data["Product_ID"] = list(range(1, len(data["TP_product"]) + 1))
#     ddf = pandas.DataFrame(data)
#
#     ax = ddf.plot.scatter(x='Product_ID', y='TP_product', c='blue', marker='o', label='TP product')
#     ax = ddf.plot.scatter(ax=ax, x='Product_ID', y='FP_product', c='red', marker='x', label='FP product')
#     plt.axhline(y=0.1, color='black', linestyle='-')
#     plt.ylabel(y_title)
#     plt.legend(loc='upper right')
#     plt.show()
#     # plt.savefig("plots.pdf")
#
#     logfile.close()


def classify_all_cases(system_paths):
    logfile = open("statistics/classified_all_cases_4.log", "w")
    all_systems = []
    for s in system_paths:
        for b in system_paths[s]:
            all_systems.append(system_paths[s][b])
    # training_systems = []

    # classify_all_cases_turn_off_testing(logfile, training_systems, testing_systems)
    # classify_all_cases_turn_off_tests_and_programs(logfile, training_systems, testing_systems)
    # classify_all_cases_turn_off_programs(logfile, training_systems, testing_systems)

    X_train, X_test, y_train, y_test, test_samples = load_all_data_cross_version(logfile, all_systems,
                                CLASSIFY_FEATURES)
    classify_by_different_classifiers(logfile, "all features", classified_all_cases_file, X_train, X_test, y_train,
                                       y_test,
                                       test_samples)
    logfile.close()


# def classify_single_bug_cases(system_paths):
#     testing_systems = []
#     for s in system_paths:
#         if "1Bug" in system_paths[s]:
#             testing_systems.append(system_paths[s]["1Bug"])
#     logfile = open("statistics/classified_single_bug_cases.log", "w")
#     X_train, X_test, y_train, y_test, test_samples = load_all_data(logfile, [], testing_systems,
#                                                                    CLASSIFY_FEATURES,
#                                                                    system_ratio=0.8, variant_ratio=0.0)
#     classify_by_different_classifiers(logfile, "all features", classified_testing_file, X_train, X_test, y_train,
#                                       y_test, test_samples)
#     logfile.close()


# def classify_by_variants(system_paths):
#     logfile = open("statistics/classified_by_variants.log", "w")
#     testing_systems = []
#     for s in system_paths:
#         for b in system_paths[s]:
#             testing_systems.append(system_paths[s][b])
#
#     X_train, X_test, y_train, y_test, test_samples = load_all_data(logfile, [], testing_systems, CLASSIFY_FEATURES,
#                                                                    0.0, 0.8)
#     classify_by_different_classifiers(logfile, "all features", classified_testing_file, X_train, X_test, y_train,
#                                       y_test, test_samples, classified_by_variant=True)
#     logfile.close()


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
        # classify_all_cases_turn_off_testing(logfile, training_set, testing_set)
        # classify_all_cases_turn_off_tests_and_programs(logfile, training_set, testing_set)
        # classify_all_cases_turn_off_programs(logfile, training_set, testing_set)
        logfile.write("---------\n")
        X_train, X_test, y_train, y_test, test_samples = load_all_for_system_edition(logfile, training_set, testing_set,
                                                                       CLASSIFY_FEATURES)
        classify_by_different_classifiers(logfile, "all features", classified_testing_file, X_train, X_test, y_train,
                                          y_test,
                                          test_samples)
    logfile.close()


# def classify_by_only_a_system(system_paths):
#     logfile = open("statistics/classified_by_only_a_system.log", "w")
#     for s in system_paths:
#         logfile.write("testing system: " + s + "\n")
#         testing_set = []
#         for bug in system_paths[s]:
#             testing_set.append(system_paths[s][bug])
#
#         logfile.write("---------\n")
#         X_train, X_test, y_train, y_test, test_samples = load_all_data(logfile, [], testing_set, CLASSIFY_FEATURES,
#                                                                        0.8, 0.0)
#         classify_by_different_classifiers(logfile, "all features", classified_testing_file, X_train, X_test, y_train,
#                                           y_test,
#                                           test_samples)
#     logfile.close()

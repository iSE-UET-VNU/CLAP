import pandas
from sklearn import svm
from sklearn import metrics

from consistent_testing_manager.FPMatricsCaculation import *
import numpy as np
from consistent_testing_manager.FileName import classified_all_file, classified_all_single_bug_file, \
    classified_all_multiple_bug_file, classified_all_testing_file

# FEATURES = [DDU,
#             not_executed_susp_stmt_vs_susp_stmt_in_passing_variant,
#             executed_susp_stmt_vs_susp_stmt_in_a_failed_execution,
#             not_executed_susp_stmt_vs_susp_stmt_in_a_failed_execution,
#             tested_unexpected_behaviors_in_passing_variant + "_0.8",
#             confirmed_successes_in_passing_variant + "_0.8",
#             total_susp_scores_in_variants,
#             both_forward_and_backward_similarity]


FEATURES = [DDU,
            executed_susp_stmt_vs_susp_stmt_in_a_failed_execution,
            not_executed_susp_stmt_vs_susp_stmt_in_a_failed_execution,
            tested_unexpected_behaviors_in_passing_variant + "_0.8",
            confirmed_successes_in_passing_variant + "_1.0",
            total_susp_scores_in_system, both_forward_and_backward_similarity, forward_similarity, backward_similarity]


def load_all_data(training_systems, testing_systems, system_ratio, variant_ratio=0):
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
        mutated_projects = list_dir(system)
        for project in mutated_projects:
            project_dir = join_path(system, project)
            consistent_testing_info_normalized_file_path = join_path(project_dir,
                                                                     consistent_testing_normalized_info_file)
            df = pandas.read_csv(consistent_testing_info_normalized_file_path)
            if system in training_systems or count < system_ratio * len(mutated_projects):
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
    train_data = train_result[FEATURES].to_numpy()
    train_target = train_result[LABEL].to_numpy()
    training_tp += np.count_nonzero(train_target == TRUE_PASSING)
    training_fp += np.count_nonzero(train_target == FALSE_PASSING)
    train_target[train_target == TRUE_PASSING] = 0
    train_target[train_target == FALSE_PASSING] = 1

    test_result = pandas.concat(test_temp)
    test_data = test_result[FEATURES].to_numpy()
    test_target = test_result[LABEL].to_numpy()
    testing_tp += np.count_nonzero(test_target == TRUE_PASSING)
    testing_fp += np.count_nonzero(test_target == FALSE_PASSING)
    test_target[test_target == TRUE_PASSING] = 0
    test_target[test_target == FALSE_PASSING] = 1

    print("training system: ", training_system)
    print("testing system: ", testing_system)
    print("Training tp: ", training_tp)
    print("Training fp:", training_fp)
    print("Testing tp:", testing_tp)
    print("Testing fp:", testing_fp)
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


def accuray_measure(y_test, y_pred):
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
    print("tp_count", TP_count)
    print("tp_correct", TP_correct)
    print("fp_count", FP_count)
    print("fp_correct", FP_correct)
    print("tp_precision", (TP_correct) / (TP_correct + FP_count - FP_correct))
    print("fp_precision", (FP_correct) / (FP_correct + TP_count - TP_correct))
    print("tp_recall", (TP_correct) / (TP_count))
    print("fp_recall", (FP_correct) / (FP_count))


def performance_in_each_projects(testing_systems, classified_file):

    for system in testing_systems:
        TP_correct = 0
        FP_correct = 0
        FP_count = 0
        TP_count = 0
        print(system)
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
        print("tp_precision", (TP_correct) / (TP_correct + FP_count - FP_correct))
        print("fp_precision", (FP_correct) / (FP_correct + TP_count - TP_correct))
        print("tp_recall", (TP_correct) / (TP_count))
        print("fp_recall", (FP_correct) / (FP_count))
        print("accuracy", (TP_correct + FP_correct)/(TP_count + FP_count))
    pass


if __name__ == "__main__":
    # training_systems = ["/Users/thu-trangnguyen/Documents/Research/SPL/Elevator/1Bug/4wise/",
    #                     "/Users/thu-trangnguyen/Documents/Research/SPL/BankAccountTP/1Bug/4wise/",
    #                     "/Users/thu-trangnguyen/Documents/Research/SPL/Email/1Bug/4wise/",
    #                     "/Users/thu-trangnguyen/Documents/Research/SPL/ExamDB/1Bug/4wise/",
    #                     "/Users/thu-trangnguyen/Documents/Research/SPL/GPL/1Bug/1wise/"]
    training_systems = [
                        ]
    testing_systems = [

        "/Users/trangnt/Documents/Projects/SPL/BankAccountTP/1Bug/4wise/",


        "/Users/trangnt/Documents/Projects/SPL/Elevator/1Bug/4wise/",


        "/Users/trangnt/Documents/Projects/SPL/Email/1Bug/4wise/",


        "/Users/trangnt/Documents/Projects/SPL/GPL/1Bug/4wise/",


        "/Users/trangnt/Documents/Projects/SPL/ZipMe/1Bug/2wise/",


        "/Users/trangnt/Documents/Projects/SPL/ExamDB/1Bug/4wise/"]

    X_train, X_test, y_train, y_test, test_samples = load_all_data(training_systems, testing_systems, 0.8, 0.0)

    clf = svm.SVC(kernel='rbf', class_weight='balanced')
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    print("Accuracy:", metrics.accuracy_score(y_test, y_pred))
    accuray_measure(y_test, y_pred)

    write_classified_result(y_pred, test_samples, 0, classified_all_testing_file)
    performance_in_each_projects(test_samples, classified_all_testing_file)

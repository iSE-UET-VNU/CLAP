import csv

from FileManager import list_dir, join_path
from consistent_testing_manager.FPMatricsCaculation import *
from consistent_testing_manager.FileName import variants_testing_label_file

if __name__ == "__main__":
    project_base_path = "/Users/thu-trangnguyen/Documents/Research/SPL/ZipMe/1Bug/2wise"
    base_features = ["BankAccount"]
    mutated_projects_list = list_dir(project_base_path)
    sum_f = 0
    sum_tp = 0
    sum_fp = 0
    for mutated_project in mutated_projects_list:
        label_file = join_path(join_path(project_base_path, mutated_project), variants_testing_label_file)

        with open(label_file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter = ',')
            for row in csv_reader:
                if row[1] == FAILING:
                    sum_f += 1
                elif row[1] == FALSE_PASSING:
                    sum_fp += 1
                elif row[1] == TRUE_PASSING:
                    sum_tp += 1

    print("failing ", sum_f/len(mutated_projects_list))
    print("false passing ", sum_fp/len(mutated_projects_list))
    print("true passing", sum_tp/len(mutated_projects_list))
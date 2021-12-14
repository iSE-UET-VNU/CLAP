import os

from FileManager import list_dir, join_path
from consistent_testing_manager.FileName import classified_all_multiple_bug_file, classified_all_file, \
    classified_all_single_bug_file, classified_all_testing_file
import shutil


def removefile(base_path, systems, bugs, kwise, file_names):
    for sys in systems:
        system_path = join_path(base_path, sys)
        for b in bugs:
            bugs_path = join_path(system_path, b)
            for k in kwise:
                kwise_path = join_path(bugs_path, k)
                if os.path.isdir(kwise_path):
                    mutated_projects_list = list_dir(kwise_path)
                    for mutated_project in mutated_projects_list:
                        mu_project_path = join_path(kwise_path, mutated_project)

                        for file in file_names:
                            file_path = join_path(mu_project_path, file)
                            print(file_path)
                            if os.path.isfile(file_path):
                                os.remove(file_path)


def get_all_mutated_projects(base_path, systems, bugs, kwise):
    f = open("all_cases.txt", "w")
    for sys in systems:
        system_path = join_path(base_path, sys)
        for b in bugs:
            bugs_path = join_path(system_path, b)
            for k in kwise:
                kwise_path = join_path(bugs_path, k)
                if os.path.isdir(kwise_path):
                    mutated_projects_list = list_dir(kwise_path)
                    for mutated_project in mutated_projects_list:
                        f.write(sys + "/" + b + "/" + k + "/" + mutated_project + "\n")
    f.close()


def remove_folder(base_path, systems, bugs, kwise):
    f = open("all_cases.txt", "r")
    contents = f.readlines()
    for sys in systems:
        system_path = join_path(base_path, sys)
        for b in bugs:
            bugs_path = join_path(system_path, b)
            for k in kwise:
                kwise_path = join_path(bugs_path, k)
                if os.path.isdir(kwise_path):
                    mutated_projects_list = list_dir(kwise_path)
                    for mutated_project in mutated_projects_list:
                        if (sys + "/" + b + "/" + k + "/" + mutated_project + "\n") not in contents:
                            try:
                                shutil.rmtree(join_path(kwise_path, mutated_project))
                            except OSError as e:
                                print("Error: %s - %s." % (e.filename, e.strerror))

if __name__ == "__main__":
    base_path = "/Users/thu-trangnguyen/Documents/Research/SPL"
    systems = ["BankAccountTP", "Elevator", "Email", "ExamDB", "GPL", "ZipMe"]
    bugs = ["1Bug", "2Bug", "3Bug"]
    kwise = ["1wise", "2wise", "3wise", "4wise"]

    #get_all_mutated_projects(base_path, systems, bugs, kwise)
    remove_folder(base_path, systems, bugs, kwise)

import os
from collections import defaultdict

from FileManager import *
import shutil


def delete_files_in_a_folder(folder_path):
   items_list = os.listdir(folder_path)
   for item in items_list:
       item_path = join_path(folder_path, item)
       if os.path.isfile(item_path):
           os.remove(item_path)
       elif os.path.isdir(item_path):
           delete_files_in_a_folder(item_path)

if __name__ == "__main__":
    system_paths = defaultdict(dict)
    system_paths["BankAccountTP"]["1Bug"] = "/Users/thu-trangnguyen/Documents/Research/SPL/BankAccountTP/1Bug/4wise/"
    system_paths["BankAccountTP"]["2Bug"] = "/Users/thu-trangnguyen/Documents/Research/SPL/BankAccountTP/2Bug/4wise/"
    system_paths["BankAccountTP"]["3Bug"] = "/Users/thu-trangnguyen/Documents/Research/SPL/BankAccountTP/3Bug/4wise/"
    system_paths["Elevator"]["1Bug"] = "/Users/thu-trangnguyen/Documents/Research/SPL/Elevator/1Bug/4wise/"
    system_paths["Elevator"]["2Bug"] = "/Users/thu-trangnguyen/Documents/Research/SPL/Elevator/2Bug/4wise/"
    system_paths["Elevator"]["3Bug"] = "/Users/thu-trangnguyen/Documents/Research/SPL/Elevator/3Bug/4wise/"
    system_paths["Email"]["1Bug"] = "/Users/thu-trangnguyen/Documents/Research/SPL/Email/1Bug/4wise/"
    system_paths["Email"]["2Bug"] = "/Users/thu-trangnguyen/Documents/Research/SPL/Email/2Bug/4wise/"
    system_paths["Email"]["3Bug"] = "/Users/thu-trangnguyen/Documents/Research/SPL/Email/3Bug/4wise/"
    system_paths["ExamDB"]["1Bug"] = "/Users/thu-trangnguyen/Documents/Research/SPL/ExamDB/1Bug/4wise/"
    system_paths["ExamDB"]["2Bug"] = "/Users/thu-trangnguyen/Documents/Research/SPL/ExamDB/2Bug/4wise/"
    system_paths["ExamDB"]["3Bug"] = "/Users/thu-trangnguyen/Documents/Research/SPL/ExamDB/3Bug/4wise/"
    system_paths["GPL"]["1Bug"] = "/Users/thu-trangnguyen/Documents/Research/SPL/GPL/1Bug/1wise/"
    system_paths["ZipMe"]["1Bug"] = "/Users/thu-trangnguyen/Documents/Research/SPL/ZipMe/1Bug/2wise/"
    for system in system_paths:
        for bug in system_paths[system]:
            path = system_paths[system][bug]
            mutated_projects = os.listdir(path)
            for project in mutated_projects:
                if ".DS" not in project:
                    project_path = join_path(path, project)
                    variants_dir = get_variants_dir(project_path)
                    variants = os.listdir(variants_dir)
                    delete_files_in_a_folder(join_path(project_path, "features"))
                    for va in variants:
                        if ".DS" not in va:
                            var_path = join_path(variants_dir, va)
                            delete_files_in_a_folder(join_path(var_path, "build"))
                            delete_files_in_a_folder(join_path(var_path, "test"))
                           


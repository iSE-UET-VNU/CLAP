import os

from FileManager import list_dir, join_path
from consistent_testing_manager.FileName import classified_all_multiple_bug_file

if __name__ == "__main__":
    project_base_path = "/Users/thu-trangnguyen/Documents/Research/SPL/ExamDB/3Bug/4wise"

    mutated_projects_list = list_dir(project_base_path)
    remove_file_names = [classified_all_multiple_bug_file]

    for mutated_project in mutated_projects_list:
        mu_project_path = join_path(project_base_path, mutated_project)

        for file in remove_file_names:
            file_path = join_path(mu_project_path, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
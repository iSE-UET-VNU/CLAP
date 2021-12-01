import os

from FileManager import list_dir, join_path

if __name__ == "__main__":
    project_base_path = "/Users/thu-trangnguyen/Documents/Research/SPL/ZipMe/1Bug/2wise"

    mutated_projects_list = list_dir(project_base_path)
    remove_file_names = ["classification_info.csv", "consistent_testing_info_normalized.csv", "consistent_testing_info.csv", "classification_info_sups_in_system.csv",
                         "ddu_info.csv", "classification_info_sups_in_variants_dependencies.csv", "classification_info_sups_in_variants.csv",
                         "classified_svc_all.csv", "classified_svc_by_a_system_0.8.csv", "classified_svc_by_system_0.6.csv", "classified_svc_by_system_0.csv",
                         "classified_svc_by_variant_0.6.csv", "classified_svc_by_variant_0.8.csv"]

    for mutated_project in mutated_projects_list:
        mu_project_path = join_path(project_base_path, mutated_project)

        for file in remove_file_names:
            file_path = join_path(mu_project_path, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
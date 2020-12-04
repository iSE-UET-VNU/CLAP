import ConfigManager
import MutantManager

from FileManager import get_project_dir, join_path, find_file_by_wildcard

if __name__ == "__main__":
    coverage_version = ""
    project_name = "Elevator-FH-JML"
    base_dir = None
    project_dir = get_project_dir(project_name, base_dir)
    sampling_output_file_path = find_file_by_wildcard(project_dir, "model.m.ca*.csv")
    optional_feature_names = ConfigManager.get_optional_feature_names(sampling_output_file_path)
    mutated_project_dirs = MutantManager.generate_mutants(project_dir, optional_feature_names, num_of_bugs=1)

import ConfigManager
import MutantManager
import TestManager
import VariantComposer

from FileManager import get_project_dir, find_file_by_wildcard, get_all_variants_dirs

if __name__ == "__main__":
    project_name = "Elevator-FH-JML"
    base_dir = ""
    project_dir = get_project_dir(project_name, base_dir)
    sampling_output_file_path = find_file_by_wildcard(project_dir, "model.m.ca*.csv")
    config_output_paths = ConfigManager.get_config_paths(project_dir, sort=True)
    variant_dirs = get_all_variants_dirs(project_dir, sort=True)
    optional_feature_names = ConfigManager.get_optional_feature_names(sampling_output_file_path)
    mutated_project_dirs = MutantManager.generate_mutants(project_dir, optional_feature_names, num_of_bugs=1)

    for mutated_project_dir in mutated_project_dirs:
        for config_path, variant_dir in zip(config_output_paths, variant_dirs):
            mutated_variant_dir = VariantComposer.compose_by_config(mutated_project_dir, config_path)
            TestManager.link_generated_junit_test_cases(variant_dir, mutated_variant_dir)

        ConfigManager.copy_configs_report(project_dir, mutated_project_dir)

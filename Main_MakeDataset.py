import AntManager
import MutantManager
import SamplingManager
import ConfigManager
import TestManager
import VariantComposer
import ModelManager

from FileManager import get_model_file_path, get_project_dir, get_dependency_lib_dirs

if __name__ == "__main__":

    # ------ START CONFIG ------
    base_dir = None
    project_name = "BankAccountTP"
    t_wise = 2
    num_of_seeding_bugs = 1
    # ------ END CONFIG ------

    project_dir = get_project_dir(project_name, base_dir)

    # get model file
    model_file_path = get_model_file_path(project_dir)

    # get jar libs
    lib_paths = get_dependency_lib_dirs(project_dir)

    # generate feature order file
    feature_order_file_path = ModelManager.generate_feature_order_file(project_dir)

    # sampling configurations
    sampling_output_file_path = SamplingManager.sampling(model_file_path, t_wise=t_wise)
    configs_report_file_path, config_output_paths = ConfigManager.generate_configs(project_dir,
                                                                                   feature_order_file_path,
                                                                                   sampling_output_file_path)

    # clone ant directory
    cloned_ant_name = AntManager.clone_ant_plugin()

    # compose and compile original feature's source code
    variant_dirs = []
    for config_path in config_output_paths:
        variant_dir = VariantComposer.compose_by_config(project_dir, config_path)
        AntManager.compile_source_classes(lib_paths=lib_paths, variant_dir=variant_dir)
        variant_dirs.append(variant_dir)

        while True:
            TestManager.generate_junit_test_cases(lib_paths=lib_paths, variant_dir=variant_dir)
            are_all_tests_passed = TestManager.run_batch_junit_test_cases(variant_dir, lib_paths=lib_paths,
                                                                          halt_on_failure=False,
                                                                          halt_on_error=False,
                                                                          custom_ant=cloned_ant_name)
            if are_all_tests_passed:
                break

    TestManager.write_test_output_to_configs_report(project_dir)

    # # generate mutants and inject them to "optional" features
    # optional_feature_names = ConfigManager.get_optional_feature_names(sampling_output_file_path)
    # mutated_project_dirs = MutantManager.generate_mutants(project_dir, optional_feature_names, num_of_seeding_bugs)
    #
    # # compile mutated feature's source code
    # for mutated_project_dir in mutated_project_dirs:
    #     for config_path, variant_dir in zip(config_output_paths, variant_dirs):
    #         mutated_variant_dir = VariantComposer.compose_by_config(mutated_project_dir, config_path)
    #         TestManager.link_generated_junit_test_cases(variant_dir, mutated_variant_dir)
    #
    #     ConfigManager.copy_configs_report(project_dir, mutated_project_dir)

import AntCompiler
import Mutant
import Sampling
import ConfigGeneration
import TestGeneration
import VariantComposer
import Model

from FileManager import get_model_file_path, get_project_dir

if __name__ == "__main__":
    project_name = "GPL-Test"
    project_dir = get_project_dir(project_name)

    # get model file
    model_file_path = get_model_file_path(project_dir)

    # generate feature order file
    feature_order_file_path = Model.generate_feature_order_file(model_file_path)

    # sampling configurations
    sampling_output_file_path = Sampling.sampling(model_file_path, t_wise=2)
    config_output_paths = ConfigGeneration.generate_configs(project_dir, feature_order_file_path,
                                                            sampling_output_file_path)

    # compile original feature's source code
    variant_dirs = []
    for config_path in config_output_paths:
        variant_dir = VariantComposer.compose_by_config(project_dir, config_path)
        AntCompiler.compile_source_classes(variant_dir)
        variant_dirs.append(variant_dir)

        TestGeneration.make_junit_test_cases(variant_dir)
        AntCompiler.compile_test_classes(variant_dir)

    # generate mutants and inject them to "optional" features
    optional_feature_names = ConfigGeneration.get_optional_feature_names(sampling_output_file_path)
    mutated_project_dirs = Mutant.generate_mutants(project_dir, optional_feature_names)

    # compile mutated feature's source code
    for config_path, variant_dir in zip(config_output_paths, variant_dirs):
        for mutated_project_dir in mutated_project_dirs:
            mutated_variant_dir = VariantComposer.compose_by_config(mutated_project_dir, config_path)
            AntCompiler.compile_source_classes(mutated_variant_dir)
            TestGeneration.link_generated_junit_test_cases(variant_dir, mutated_variant_dir)

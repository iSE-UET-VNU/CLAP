import AntCompiler
import Mutant
import Sampling
import GenerateConfiguration
import VariantComposer
import Model

from FileManager import get_model_file_path, get_project_dir

BASE_DIR = "projects"

if __name__ == "__main__":
    project_name = "GPL-Test"
    project_dir = get_project_dir(project_name)
    # get model file
    model_file_path = get_model_file_path(project_dir)

    # generate feature order file
    feature_order_file_path = Model.generate_feature_order_file(model_file_path)

    # sampling configurations
    sampling_output_file_path = Sampling.sampling(model_file_path, t_wise=2)
    config_output_paths = GenerateConfiguration.generate_configs(feature_order_file_path, sampling_output_file_path)

    # compile original feature's source code
    for config_path in config_output_paths:
        variant_source_code_dir = VariantComposer.compose_by_config(config_path, project_dir)
        AntCompiler.compile_classes(variant_source_code_dir)
    #
    # # generate mutants and inject them to "optional" features
    # optional_feature_names = GenerateConfiguration.get_optional_feature_names(sampling_output_file_path)
    # mutated_project_dirs = Mutant.generate_mutants(project_dir, optional_feature_names)
    #
    # # compile mutated feature's source code
    # for config_path in config_output_paths:
    #     for mutated_project_dir in mutated_project_dirs:
    #         VariantComposer.compose_by_config(config_path, mutated_project_dir)

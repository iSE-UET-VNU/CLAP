import Sampling
import GenerateConfiguration
import VariantCompiler
import Model

from FileManager import get_model_file_path, get_project_dir

BASE_DIR = "projects"

if __name__ == "__main__":
    project_name = "HelloWorld-FH-Java-Test"
    project_dir = get_project_dir(project_name)
    model_file_path = get_model_file_path(project_dir)
    feature_order_file_path = Model.generate_feature_order_file(model_file_path)
    sampling_output_file_path = Sampling.sampling(model_file_path, t_wise=2)
    config_output_paths = GenerateConfiguration.generate_variants(feature_order_file_path, sampling_output_file_path)
    for config_path in config_output_paths:
        VariantCompiler.compile_by_config(config_path)
    # GenerateMutant.generateMutants("D:\Configurable Systems\mujava_results")

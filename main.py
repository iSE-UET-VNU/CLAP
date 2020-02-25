import Sampling
import GenerateConfiguration
import VariantCompiler
from os import path

from FileManager import get_model_file_path

if __name__ == "__main__":
    project_dir = "projects/HelloWorld-FH-Java-Test"
    model_file_path = get_model_file_path(project_dir)
    sampling_output_file_path = Sampling.sampling(model_file_path, t_wise=2)
    # sampling_output_file_path = "static/gpl_model.m.ca2.csv"
    config_output_paths = GenerateConfiguration.generate_variants(sampling_output_file_path)
    for config_path in config_output_paths:
        VariantCompiler.compile_by_config(config_path)
    # generate mutants
    # GenerateMutant.generateMutants("D:\Configurable Systems\mujava_results")

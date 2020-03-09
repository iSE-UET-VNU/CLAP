import AntCompiler
import Mutant
import Sampling
import ConfigGeneration
import TestGeneration
import VariantComposer

from FileManager import get_project_dir

if __name__ == "__main__":
    project_name = "GPL-Test"
    project_dir = get_project_dir(project_name)

    # get configs
    config_paths = ConfigGeneration.get_config_paths(project_dir)

    # get mutated_variant
    mutated_project_dirs = Mutant.get_mutated_project_dirs(project_dir)
    for mutated_project_dir in mutated_project_dirs:
        TestGeneration.generate_junit_test_output_report(mutated_project_dir)

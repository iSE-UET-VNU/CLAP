import re

from FileManager import get_plugin_path, get_variant_dir, get_feature_source_code_dir, move_file, \
    get_file_name, join_path, is_path_exist, get_compiled_classes_dir, get_test_cases_dir
from Helpers import get_logger, execute_shell_command

logger = get_logger(__name__)

PLUGIN_NAME = "evosuite-1.0.6.jar"
PLUGIN_PATH = get_plugin_path(PLUGIN_NAME)


def make_junit_test_cases(project_dir):
    logger.info(f"Generating JUnit Test for project [{get_file_name(project_dir)}]")
    compiled_classes_dir = get_compiled_classes_dir(project_dir)
    test_cases_dir = get_test_cases_dir(project_dir)
    output_log = execute_shell_command(f'java -jar {PLUGIN_PATH}', extra_args=[
        {"-projectCP": compiled_classes_dir},
        {"-seed": 1583738192420},
        {"-target": compiled_classes_dir},
        {"-continuous": "execute"},
        {"-Dctg_memory": "4000"},
        {"-Dctg_cores": "4"},
        {"-Dctg_export_folder": test_cases_dir},
    ], show_log_path=True)

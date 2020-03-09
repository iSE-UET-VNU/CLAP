import re

from FileManager import get_plugin_path, get_variant_dir, get_feature_source_code_dir, move_file, \
    get_file_name, join_path, is_path_exist
from Helpers import get_logger, execute_shell_command

logger = get_logger(__name__)

PLUGIN_NAME = "evosuite-1.0.6.jar"
PLUGIN_PATH = get_plugin_path(PLUGIN_NAME)


def run(project_dir):
    logger.info(
        f"Generating JUnit Test for project [{get_file_name(project_dir)}]")
    config_name = get_file_name(config_file_path)
    output_dir = get_variant_dir(project_dir, config_name)
    execute_shell_command(f'java -jar {PLUGIN_PATH}', extra_args=[
        {"--expression": config_file_path},
        {"--base-directory": get_feature_source_code_dir(project_dir)},
        {"--output-directory": output_dir},
        {"--export_roles_json": ""}
    ])
    output_src_dir = join_path(output_dir, config_name)
    if is_path_exist(output_src_dir):
        renamed_folder_dir = join_path(output_dir, "src")
        move_file(output_src_dir, renamed_folder_dir)
    return output_dir

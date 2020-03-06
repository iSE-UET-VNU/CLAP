import re

from FileManager import get_plugin_path, get_variant_dir, get_outer_dir, get_feature_source_code_dir, move_file, \
    get_file_name, join_path, is_path_exist
from Helpers import get_logger, execute_shell_command

logger = get_logger(__name__)

PLUGIN_NAME = "FeatureHouse_2020.jar"
PLUGIN_PATH = get_plugin_path(PLUGIN_NAME)


def get_sampling_file_path(stdout):
    return re.search("(?<=Wrote result to )[^\n]+", stdout).group()


def compile_by_config(config_file_path, project_dir):
    logger.info(f"Compiling [{get_file_name(project_dir)}] source code with config file [{get_file_name(config_file_path)}]")
    config_name = get_file_name(config_file_path)
    output_dir = get_variant_dir(project_dir, config_name)
    output_log = execute_shell_command(f'java -jar {PLUGIN_PATH}', extra_args=[
        {"--expression": config_file_path},
        {"--base-directory": get_feature_source_code_dir(project_dir)},
        {"--output-directory": output_dir},
        {"--export_roles_json": ""}
    ])
    output_src_dir = join_path(output_dir, config_name)
    if is_path_exist(output_src_dir):
        renamed_folder_dir = join_path(output_dir, "src")
        move_file(output_src_dir, renamed_folder_dir)
    return output_log

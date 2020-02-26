import os
import re

from FileManager import get_plugin_path, get_variant_dir, get_outer_dir, get_feature_source_code_dir, move_file
from Helpers import get_logger, execute_shell_command

logger = get_logger(__name__)


def get_sampling_file_path(stdout):
    return re.search("(?<=Wrote result to )[^\n]+", stdout).group()


def compile_by_config(config_file_path):
    plugin_name = "FeatureHouse_2020.jar"
    plugin_path = get_plugin_path(plugin_name)
    logger.info(f"Compiling code with config file [{config_file_path}]")
    project_dir = get_outer_dir(config_file_path, step=2)
    config_name = get_file_name(config_file_path)
    output_dir = get_variant_dir(project_dir, config_name)
    output_log = execute_shell_command(f'java -jar {plugin_path}', extra_args=[
        {"--expression": config_file_path},
        {"--base-directory": get_feature_source_code_dir(project_dir)},
        {"--output-directory": output_dir},
        {"--export_roles_json": ""}
    ])
    output_src_dir = os.path.join(output_dir, config_name)
    if os.path.exists(output_src_dir):
        renamed_folder_dir = os.path.join(output_dir, "src")
        move_file(output_src_dir, renamed_folder_dir)
    return output_log

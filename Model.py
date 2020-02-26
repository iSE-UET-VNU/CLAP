import os

from FileManager import get_plugin_path, get_outer_dir
from Helpers import get_logger, execute_shell_command

logger = get_logger(__name__)


def generate_feature_order_file(model_file_path):
    plugin_name = "FeatureOrderTool.jar"
    plugin_path = get_plugin_path(plugin_name)
    logger.info(f"Generating Feature Order file from model file [{model_file_path}]")
    output_feature_order_path = os.path.join(get_outer_dir(model_file_path), "features.order")
    execute_shell_command(f'java -jar {plugin_path} ', extra_args=[
        {"--feature_model": model_file_path},
        {"--output_feature_order_path": output_feature_order_path},
    ])
    return output_feature_order_path


def read_feature_order_file(file_path):
    with open(file_path) as input_file:
        feature_list = [line.strip() for line in input_file.readlines()]
        return feature_list

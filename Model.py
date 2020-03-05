from FileManager import get_plugin_path, get_outer_dir, join_path
from Helpers import get_logger, execute_shell_command

logger = get_logger(__name__)

PLUGIN_NAME = "FeatureOrderTool.jar"
PLUGIN_PATH = get_plugin_path(PLUGIN_NAME)


def generate_feature_order_file(model_file_path):
    logger.info(f"Generating Feature Order file from model file [{model_file_path}]")
    output_feature_order_path = join_path(get_outer_dir(model_file_path), "features.order")
    execute_shell_command(f'java -jar {PLUGIN_PATH} ', extra_args=[
        {"--feature_model": model_file_path},
        {"--output_feature_order_path": output_feature_order_path},
    ])
    return output_feature_order_path


def read_feature_order_file(file_path):
    with open(file_path) as input_file:
        feature_list = [line.strip() for line in input_file.readlines()]
        return feature_list

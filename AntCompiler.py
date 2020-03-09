from FileManager import get_plugin_path, get_file_name, get_src_dir, get_output_classes_dir
from Helpers import get_logger, execute_shell_command

logger = get_logger(__name__)

PLUGIN_NAME = "java_builder.sh"
PLUGIN_PATH = get_plugin_path(PLUGIN_NAME)


def compile_classes(variant_dir):
    logger.info(f"Compiling source code [{get_file_name(variant_dir)}] ")
    output_log = execute_shell_command(f'/bin/sh {PLUGIN_PATH}', extra_args=[
        {"-src": get_src_dir(variant_dir)},
        {"-out": get_output_classes_dir(variant_dir)},
    ])
    return output_log

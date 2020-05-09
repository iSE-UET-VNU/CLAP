from FileManager import get_plugin_path, get_file_name_with_parent, get_slicing_log_file_path, get_outer_dir
from Helpers import get_logger, execute_shell_command

logger = get_logger(__name__)

PLUGIN_NAME = "feature-slicing.jar"
PLUGIN_PATH = get_plugin_path(PLUGIN_NAME)


def do_slice(spc_file_path):
    slicing_output_path = get_slicing_log_file_path(get_outer_dir(spc_file_path))
    logger.info(f"Running slicing from spc file [{get_file_name_with_parent(spc_file_path)}]")
    output_log = execute_shell_command(
        f'java -Dspc_path={spc_file_path} -Dslicing_output_path={slicing_output_path} -jar {PLUGIN_PATH} ',
        extra_args=[])
    logger.info(f"Wrote slicing output to file [{get_file_name_with_parent(slicing_output_path)}]")

import logging
import time

from FileManager import get_plugin_path, get_file_name_with_parent, get_slicing_log_file_path, get_outer_dir, \
    get_spectrum_failed_coverage_file_name_with_version, is_path_exist, get_slicing_test_case_output_file_path
from Helpers import get_logger, execute_shell_command

logger = get_logger(__name__)

FEATURE_SLICING_PLUGIN_NAME = "feature-slicing.jar"
FEATURE_SLICING_PLUGIN_PATH = get_plugin_path(FEATURE_SLICING_PLUGIN_NAME)

TEST_CASE_SLICING_PLUGIN_NAME = "testcase-slicing.jar"
TEST_CASE_SLICING_PLUGIN_PATH = get_plugin_path(TEST_CASE_SLICING_PLUGIN_NAME)


def do_slice_spc(spc_file_path, filtering_coverage_rate, coverage_version):
    start_time = time.time()

    failed_coverage_file_name = get_spectrum_failed_coverage_file_name_with_version(version=coverage_version)

    if (coverage_version != ""):
        post_fix = str(filtering_coverage_rate) + "_" + coverage_version + "_"
    else:
        post_fix = filtering_coverage_rate
    slicing_output_path = get_slicing_log_file_path(get_outer_dir(spc_file_path), post_fix)
    if is_path_exist(slicing_output_path):
        logger.info(f"Used Old Slicing log file [{slicing_output_path}]")
        return 0

    logger.info(f"Running suspicious_statements_manager from spc file [{get_file_name_with_parent(spc_file_path)}]")
    output_log = execute_shell_command(
        f'java -Xmx256m -Dspc_path={spc_file_path} -Dslicing_output_path={slicing_output_path} -Dcoverage_file_name={failed_coverage_file_name} -jar {FEATURE_SLICING_PLUGIN_PATH} ',
        extra_args=[], log_to_file=True)
    logger.info(
        f"Wrote suspicious_statements_manager output to file [{get_file_name_with_parent(slicing_output_path)}]")
    logging.info("[Runtime] suspicious_statements_manager %s: %s", slicing_output_path, time.time() - start_time)
    slicing_runtime = time.time() - start_time
    return slicing_runtime


def do_slice_pts(pts_file_path):
    failed_coverage_file_name = get_spectrum_failed_coverage_file_name_with_version(version="")
    output_path = get_slicing_test_case_output_file_path(get_outer_dir(pts_file_path))

    if is_path_exist(output_path):
        logger.info(f"Used Old Slicing log file [{output_path}]")
        return output_path

    logger.info(
        f"Running [SLICE-BASED] slicing on test cases from pts file [{get_file_name_with_parent(pts_file_path)}]")
    output_log = execute_shell_command(
        f'java -Xmx256m -Dpts_path={pts_file_path} -Dslicing_output_path={output_path} -Dcoverage_file_name={failed_coverage_file_name} -jar {TEST_CASE_SLICING_PLUGIN_PATH} ',
        extra_args=[], log_to_file=True)
    print(output_log)
    logger.info(
        f"Wrote SLICE-BASED] slicing on test cases output to file [{get_file_name_with_parent(output_path)}]")
    return output_path

from FileManager import get_plugin_path, get_file_name_with_parent, get_test_coverage_dir, join_path, \
    FAILED_TEST_COVERAGE_FOLDER_NAME, PASSED_TEST_COVERAGE_FOLDER_NAME, \
    is_path_exist, get_all_variants_dirs, get_passed_spectrum_coverage_file_path_with_version, \
    get_failed_spectrum_coverage_file_path_with_version
from Helpers import get_logger, execute_shell_command, get_version_by_time

logger = get_logger(__name__)

PLUGIN_NAME = "testcase_finder.jar com.nkt.coverage.SpectrumCoverageConverter"
PLUGIN_PATH = get_plugin_path(PLUGIN_NAME)


def rebuild_spectrum_coverage_for_mutated_project(mutated_project_dir, version=""):
    if not version:
        version = get_version_by_time()
    random = False
    variant_dirs = get_all_variants_dirs(mutated_project_dir)
    for variant_dir in variant_dirs:
        rebuild_spectrum_coverage_for_variant(variant_dir, version=version, random=random)


def rebuild_spectrum_coverage_for_variant(variant_dir, version="", random=True):
    test_coverage_dir = get_test_coverage_dir(variant_dir)
    failed_coverage_dir = join_path(test_coverage_dir, FAILED_TEST_COVERAGE_FOLDER_NAME)
    if is_path_exist(failed_coverage_dir):
        spectrum_failed_coverage_file_path = get_failed_spectrum_coverage_file_path_with_version(variant_dir, version)
        rebuild_spectrum_coverage(input_coverage_dir=failed_coverage_dir,
                                  spectrum_output_path=spectrum_failed_coverage_file_path, random=random,
                                  max_test_cases=10)

    passed_coverage_dir = join_path(test_coverage_dir, PASSED_TEST_COVERAGE_FOLDER_NAME)
    if is_path_exist(passed_coverage_dir):
        spectrum_passed_coverage_file_path = get_passed_spectrum_coverage_file_path_with_version(variant_dir, version)
        rebuild_spectrum_coverage(input_coverage_dir=passed_coverage_dir,
                                  spectrum_output_path=spectrum_passed_coverage_file_path, random=random)


def rebuild_spectrum_coverage(input_coverage_dir, spectrum_output_path, random=True, max_test_cases=-1):
    if is_path_exist(spectrum_output_path):
        logger.info(f"Ignoring spectrum coverage file for [{get_file_name_with_parent(input_coverage_dir)}]")
        return
    logger.info(f"Building spectrum coverage file for [{get_file_name_with_parent(input_coverage_dir)}]")
    output_log = execute_shell_command(
        f'java -Xmx128m -Drandom={str(random).lower()} -Dupper_bound={max_test_cases} -Dcoverage_dir={input_coverage_dir} -Doutput_path={spectrum_output_path} -cp {PLUGIN_PATH} ',
        extra_args=[], log_to_file=True)
    print(output_log)

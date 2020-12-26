import TestingCoverageManager
from FileManager import get_plugin_path, get_file_name_with_parent, get_test_coverage_dir, join_path, \
    FAILED_TEST_COVERAGE_FOLDER_NAME, PASSED_TEST_COVERAGE_FOLDER_NAME, \
    is_path_exist, get_all_variant_dirs, get_passed_spectrum_coverage_file_path_with_version, \
    get_failed_spectrum_coverage_file_path_with_version, get_failed_test_coverage_dir, get_passed_test_coverage_dir
from Helpers import get_logger, execute_shell_command, get_version_by_time

logger = get_logger(__name__)

PLUGIN_NAME = "testcase_finder.jar com.nkt.coverage.SpectrumCoverageConverter"
PLUGIN_PATH = get_plugin_path(PLUGIN_NAME)


# BUILD TEST COVERAGE WITH RANDOM TEST CASES

def rebuild_spectrum_coverage_for_mutated_project(mutated_project_dir, version=""):
    if not version:
        version = get_version_by_time()
    random = True
    variant_dirs = get_all_variant_dirs(mutated_project_dir)
    for variant_dir in variant_dirs:
        rebuild_spectrum_coverage_for_variant(variant_dir, version=version, random=random)


def rebuild_spectrum_coverage_for_variant(variant_dir, version="", random=True):
    test_coverage_dir = get_test_coverage_dir(variant_dir)
    failed_coverage_dir = join_path(test_coverage_dir, FAILED_TEST_COVERAGE_FOLDER_NAME)
    if is_path_exist(failed_coverage_dir):
        spectrum_failed_coverage_file_path = get_failed_spectrum_coverage_file_path_with_version(test_coverage_dir,
                                                                                                 version)
        rebuild_spectrum_coverage(input_coverage_dir=failed_coverage_dir,
                                  spectrum_output_path=spectrum_failed_coverage_file_path, random=random,
                                  max_test_cases=10)

    passed_coverage_dir = join_path(test_coverage_dir, PASSED_TEST_COVERAGE_FOLDER_NAME)
    if is_path_exist(passed_coverage_dir):
        spectrum_passed_coverage_file_path = get_passed_spectrum_coverage_file_path_with_version(test_coverage_dir,
                                                                                                 version)
        rebuild_spectrum_coverage(input_coverage_dir=passed_coverage_dir,
                                  spectrum_output_path=spectrum_passed_coverage_file_path, random=random)


# BUILD TEST COVERAGE FROM SPECIFIC TEST CASES


def rebuild_spectrum_coverage_with_target_coverage(mutated_project_dir, target_coverage):
    # rebuild_failed_spectrum_coverage_from_specific_test_cases(test_coverage_dir=coverage_dir, test_cases=["EmailSystem.Client_ESTest.test19.coverage.xml", "EmailSystem.Client_ESTest.test55.coverage.xml"])

    """
    require all variants to have the same coverage level
    interrupt immediately if no solution found for a specific variant
    """

    mutated_variant_dirs = get_all_variant_dirs(mutated_project_dir, sort=True)
    test_coverage_container = []
    version = f"test_{target_coverage}"

    # find optimal test cases
    for mutated_variant_dir in mutated_variant_dirs[:]:
        if True or "model_m_ca4_0004" in mutated_variant_dir:
            print("-" * 20)
            print(mutated_variant_dir)
            test_coverage_dir = get_test_coverage_dir(mutated_variant_dir)
            failed_test_coverage_dir = get_failed_test_coverage_dir(mutated_variant_dir)
            passed_test_coverage_dir = get_passed_test_coverage_dir(mutated_variant_dir)
            optimal_coverage_file_path_dict = TestingCoverageManager.find_optimal_test_cases_with_target_coverage(
                failed_test_coverage_dir,
                passed_test_coverage_dir,
                target_coverage=target_coverage)
            if not optimal_coverage_file_path_dict:
                return
            else:
                test_coverage_container.append((test_coverage_dir, optimal_coverage_file_path_dict))

    # build spectrum coverage based on optimal test cases
    for item in test_coverage_container:
        test_coverage_dir, optimal_coverage_file_path_dict = item
        failed_test_cases = optimal_coverage_file_path_dict.get(FAILED_TEST_COVERAGE_FOLDER_NAME)
        if failed_test_cases:
            # print(test_coverage_dir, failed_test_cases)
            rebuild_failed_spectrum_coverage_from_specific_test_cases(test_coverage_dir, failed_test_cases, version)
        passed_test_cases = optimal_coverage_file_path_dict.get(PASSED_TEST_COVERAGE_FOLDER_NAME)
        if passed_test_cases:
            # print(test_coverage_dir, passed_test_cases)
            rebuild_passed_spectrum_coverage_from_specific_test_cases(test_coverage_dir, passed_test_cases, version)


def rebuild_failed_spectrum_coverage_from_specific_test_cases(test_coverage_dir, test_cases, version=""):
    if not version:
        version = get_version_by_time()
    return rebuild_spectrum_coverage_from_specific_test_cases(test_coverage_dir=test_coverage_dir,
                                                              by_test_result_folder_name=FAILED_TEST_COVERAGE_FOLDER_NAME,
                                                              test_cases=test_cases, version=version)


def rebuild_passed_spectrum_coverage_from_specific_test_cases(test_coverage_dir, test_cases, version=""):
    if not version:
        version = get_version_by_time()
    return rebuild_spectrum_coverage_from_specific_test_cases(test_coverage_dir=test_coverage_dir,
                                                              by_test_result_folder_name=PASSED_TEST_COVERAGE_FOLDER_NAME,
                                                              test_cases=test_cases, version=version)


def rebuild_spectrum_coverage_from_specific_test_cases(test_coverage_dir, by_test_result_folder_name, test_cases,
                                                       version=""):
    by_result_coverage_dir = join_path(test_coverage_dir, by_test_result_folder_name)
    if is_path_exist(by_result_coverage_dir):
        if by_test_result_folder_name == FAILED_TEST_COVERAGE_FOLDER_NAME:
            spectrum_coverage_file_path = get_failed_spectrum_coverage_file_path_with_version(test_coverage_dir,
                                                                                              version)
        else:
            spectrum_coverage_file_path = get_passed_spectrum_coverage_file_path_with_version(test_coverage_dir,
                                                                                              version)
        rebuild_spectrum_coverage(input_coverage_dir=by_result_coverage_dir,
                                  spectrum_output_path=spectrum_coverage_file_path,
                                  specific_test_cases=test_cases,
                                  random=False,
                                  max_test_cases=-1)


def rebuild_spectrum_coverage(input_coverage_dir, spectrum_output_path, specific_test_cases=None, random=True,
                              max_test_cases=-1):
    if is_path_exist(spectrum_output_path):
        logger.info(f"Ignoring spectrum coverage file for [{get_file_name_with_parent(input_coverage_dir)}]")
        return
    if isinstance(specific_test_cases, list):
        joined_test_cases = ",".join(specific_test_cases)
    else:
        joined_test_cases = ""
    logger.info(f"Building spectrum coverage file for [{get_file_name_with_parent(input_coverage_dir)}]")
    output_log = execute_shell_command(
        f'java -Xmx128m -Drandom={str(random).lower()} -Dupper_bound={max_test_cases} -Dtest_cases={joined_test_cases} -Dcoverage_dir={input_coverage_dir} -Doutput_path={spectrum_output_path} -cp {PLUGIN_PATH} ',
        extra_args=[], log_to_file=True)
    print(output_log)

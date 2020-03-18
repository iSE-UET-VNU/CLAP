import csv
import re

from FileManager import get_plugin_path, get_file_name, get_test_dir, create_symlink, get_compiled_source_classes_dir, \
    get_compiled_test_classes_dir, list_dir, get_variants_dir, get_src_dir, get_test_results_dir, \
    get_test_coverage_dir, get_variant_dir, is_path_exist, join_path, get_model_configs_report_path
from Helpers import get_logger, execute_shell_command

logger = get_logger(__name__)

EVOSUITE_PLUGIN_NAME = "evosuite-1.0.6.jar"
EVOSUITE_PLUGIN_PATH = get_plugin_path(EVOSUITE_PLUGIN_NAME)

JUNIT_PLUGIN_NAME = "es_junit.sh"
JUNIT_PLUGIN_PATH = get_plugin_path(JUNIT_PLUGIN_NAME)


def make_junit_test_cases(variant_dir):
    logger.info(f"Generating JUnit Test for variant [{get_file_name(variant_dir)}]")
    compiled_classes_dir = get_compiled_source_classes_dir(variant_dir)
    test_cases_dir = get_test_dir(variant_dir)
    output_log = execute_shell_command(f'java -jar {EVOSUITE_PLUGIN_PATH}', extra_args=[
        {"-projectCP": compiled_classes_dir},
        {"-seed": 1583738192420},
        {"-target": compiled_classes_dir},
        {"-continuous": "execute"},
        {"-Dctg_memory": "4000"},
        {"-Dctg_cores": "4"},
        {"-Dctg_export_folder": test_cases_dir},
        {"-Dno_runtime_dependency": "true"},
    ], log_to_file=True)


def link_generated_junit_test_cases(variant_dir, target_variant_dir):
    logger.info(f"Linking JUnit Test for variant [{get_file_name(variant_dir)}]")
    generated_test_dir = get_test_dir(variant_dir)
    target_test_dir = get_test_dir(target_variant_dir)
    create_symlink(generated_test_dir, target_test_dir)


def run_junit_test_cases_with_coverage(variant_dir, halt_on_failure=False, halt_on_error=True):
    logger.info(f"Running JUnit Test for variant [{get_file_name(variant_dir)}]")
    src_dir = get_src_dir(variant_dir)
    test_dir = get_test_dir(variant_dir)
    src_classes_dir = get_compiled_source_classes_dir(variant_dir)
    test_classes_dir = get_compiled_test_classes_dir(variant_dir)
    test_coverage_dir = get_test_coverage_dir(variant_dir)
    output_log = execute_shell_command(f'/bin/sh {JUNIT_PLUGIN_PATH}', extra_args=[
        {"-src": src_dir},
        {"-test": test_dir},
        {"-build.classes": src_classes_dir},
        {"-build.testclasses": test_classes_dir},
        {"-report.coveragedir": test_coverage_dir},
        {"-junit.haltonfailure": "yes" if halt_on_failure else "no"},
    ], log_to_file=True)
    is_test_failure = re.search("(Failures: 1|Errors: 1|BUILD FAILED)", output_log)
    if is_test_failure:
        if halt_on_failure or (halt_on_error and "Errors" in is_test_failure.group()) or "BUILD FAILED" in is_test_failure.group():
            logger.fatal("Some test cases were failed, see log for more detail\n{}".format(output_log))
        return False
    return True


def generate_junit_test_output_report(project_dir):
    variants_dir = get_variants_dir(project_dir)
    for variant_dir in list_dir(variants_dir, full_path=True):
        is_passed = run_junit_test_cases_with_coverage(variant_dir)


def check_variant_final_test_output(variant_dir):
    coverage_dir = get_test_coverage_dir(variant_dir)
    if is_path_exist(join_path(coverage_dir, "failed")):
        return False
    elif is_path_exist(join_path(coverage_dir, "passed")):
        return True
    else:
        return None


def write_test_output_to_configs_report(project_dir):
    logger.info(f"Writing test output to project's configs report [{get_file_name(project_dir)}]")
    configs_report_file_path = get_model_configs_report_path(project_dir)
    rows = []
    with open(configs_report_file_path, "r") as report_csv:
        reader = csv.reader(report_csv)
        for i, row in enumerate(reader):
            rows.append(row)
            if i == 0:
                continue
            config_name = row[0]
            variant_dir = get_variant_dir(project_dir, config_name)
            final_test_output = check_variant_final_test_output(variant_dir)
            if final_test_output is True:
                row[-1] = "__PASSED__"
            elif final_test_output is False:
                row[-1] = "__FAILED__"
    with open(configs_report_file_path, "w") as output_report_csv:
        writer = csv.writer(output_report_csv)
        writer.writerows(rows)

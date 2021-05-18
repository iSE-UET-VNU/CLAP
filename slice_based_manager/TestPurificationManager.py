import re
from collections import defaultdict

from bs4 import BeautifulSoup, NavigableString

from FileManager import get_junit_report_path, SOURCE_CODE_EXTENSION, get_test_dir, join_path, \
    get_file_name_without_ext, copy_dir, get_src_dir, get_temp_src_dir, get_outer_dir, \
    TEST_FOLDER_NAME, TEMP_SRC_FOLDER_NAME, get_purified_test_suites_report_path, get_file_name
from Helpers import get_logger

logger = get_logger(__name__)


def generate_purified_test_suite(mutated_project_dir, failed_variant_dirs):
    purified_test_suites_report_dict = {}
    for failed_variant_dir in failed_variant_dirs:
        failed_test_info_list = get_failed_test_info_from_junit_report(failed_variant_dir)
        temp_src_dir = init_temp_src(failed_variant_dir)
        assertion_line_container = generate_purified_test_cases_source_code(failed_variant_dir, failed_test_info_list)
        purified_test_suites_report_dict[temp_src_dir] = assertion_line_container

    write_purified_test_suites_report_dict(mutated_project_dir, purified_test_suites_report_dict)


def write_purified_test_suites_report_dict(mutated_project_dir, test_suites_report_dict):
    output_path = get_purified_test_suites_report_path(mutated_project_dir)
    with open(output_path, "w+") as output_file:
        for temp_src_dir, assertion_line_numbers in test_suites_report_dict.items():
            output_file.write("{};{}\n".format(",".join(assertion_line_numbers), temp_src_dir))
    logger.info(f"Done to write purified test suites to [{get_file_name(mutated_project_dir)}]")


def init_temp_src(failed_variant_dir):
    src_dir = get_src_dir(failed_variant_dir)
    new_src_dir = get_temp_src_dir(failed_variant_dir)
    copy_dir(src_dir, new_src_dir, delete_existing_dir=True)
    return new_src_dir


def generate_purified_test_cases_source_code(failed_variant_dir, failed_test_info_list):
    # find raw failed test case, obtain source code and purify all
    test_case_source_code_dict = defaultdict(list)
    required_import_statements_container_dict = {}
    for test_case_info in failed_test_info_list:
        test_file_path, required_import_statements, purified_test_case_source_code = purify_test_case(test_case_info)
        required_import_statements_container_dict[test_file_path] = required_import_statements
        test_case_source_code_dict[test_file_path].append(purified_test_case_source_code)

    # compose new test case files and write to temp_src/
    assertion_line_container = []
    new_test_file_path_container = []
    for test_file_path in test_case_source_code_dict:
        required_import_statements = required_import_statements_container_dict[test_file_path]
        source_code_list = test_case_source_code_dict[test_file_path]
        new_test_class_name, assertion_line_numbers, composed_test_suite_source_code = compose_purified_test_suite(
            test_file_path, required_import_statements, source_code_list)

        new_test_file_path = save_purified_test_suite(failed_variant_dir, new_test_class_name, test_file_path,
                                                      composed_test_suite_source_code)
        new_test_file_path_container.append(new_test_file_path)
        assertion_line_container.extend(assertion_line_numbers)

    return assertion_line_container


def save_purified_test_suite(failed_variant_dir, new_test_class_name, old_test_file_path,
                             composed_test_suite_source_code):
    # write new test file to temp_src/ for providing simple slicing (without needing to import JUnit)
    new_test_file_path = join_path(get_outer_dir(old_test_file_path), new_test_class_name + SOURCE_CODE_EXTENSION)
    new_test_file_path = new_test_file_path[:len(failed_variant_dir)] + re.sub(f"^/{TEST_FOLDER_NAME}/(main/)?",
                                                                               f"/{TEMP_SRC_FOLDER_NAME}/",
                                                                               new_test_file_path[
                                                                               len(failed_variant_dir):])
    with open(new_test_file_path, "w+") as output_file:
        output_file.write(composed_test_suite_source_code)
    return new_test_file_path


PURIFIED_TEST_SUITE_NAME = "CustomTestSuiteX"

PREDEFINE_SOURCE_CODE = """
    public static void assertTrue(boolean condition) { }

    public static void assertFalse(boolean condition) { }
    
    public static void assertEquals(Object expected, Object actual) { } 
    
    public static void assertNotEquals(Object unexpected, Object actual) { }
    
    public static void assertNotNull(Object object) { }

    public static void assertNull(String message, Object object) { }
    
    public static class Random{ public static void setNextRandom(int number) { }}
"""

PURIFIED_TEST_SUITE_SOURCE_CODE_TEMPLATE = f"""
%s

public class %s {{\n\n   %s   

{PREDEFINE_SOURCE_CODE}
}}
"""


def compose_purified_test_suite(test_file_path, required_import_statements_container, test_case_source_code_container):
    old_test_class_name = get_file_name_without_ext(test_file_path)
    new_test_class_name = f"{PURIFIED_TEST_SUITE_NAME}_{old_test_class_name}"
    full_source_code = PURIFIED_TEST_SUITE_SOURCE_CODE_TEMPLATE % (
        "\n".join(required_import_statements_container),
        new_test_class_name,
        "\n\n   ".join(test_case_source_code_container))
    source_code_lines = full_source_code.splitlines()
    package_name = source_code_lines[1].split(" ", 1)[1].strip(";")
    qualified_class_name = package_name + "." + new_test_class_name
    assertion_line_numbers = [f"{qualified_class_name}.{i + 1}" for i, line in enumerate(full_source_code.splitlines())
                              if
                              "//_X_FAILED_ASSERTION_" in line]
    return new_test_class_name, assertion_line_numbers, full_source_code


TEST_CASE_METHOD_SIGNATURE_TEMPLATE = "public void {test_case_name}()  throws Throwable"


def purify_test_case(failed_test_info):
    test_file_path = failed_test_info[0]
    test_case_name = failed_test_info[1]
    failed_assertion_line_number = failed_test_info[2]

    all_test_source_code_lines = open(failed_test_info[0]).read().splitlines()

    # prune import statements
    required_import_statements = []
    for line in all_test_source_code_lines:
        if line.startswith("package") and not required_import_statements:
            required_import_statements.append(line)
        if line.startswith("import"):
            target_package = line.split(" ")[-1]
            if not target_package.startswith("org.junit") and not target_package.startswith("org.evosuite"):
                required_import_statements.append(line)
        if line.startswith("@RunWith(EvoRunner.class)"):
            break

    # prune assertion statement
    test_case_method_signature = TEST_CASE_METHOD_SIGNATURE_TEMPLATE.format(test_case_name=test_case_name)
    if 'fail("Expecting exception' in all_test_source_code_lines[failed_assertion_line_number - 1]:
        if "try {" in all_test_source_code_lines[failed_assertion_line_number - 3]:
            all_test_source_code_lines.pop(failed_assertion_line_number - 3)
            failed_assertion_line_number = failed_assertion_line_number - 2
        else:
            raise Exception(
                f"Found [fail()] statement but is not surrounded by try-catch [{test_file_path}][{test_case_name}]")
    elif "try {" in all_test_source_code_lines[failed_assertion_line_number - 2]:
        all_test_source_code_lines.pop(failed_assertion_line_number - 2)
        failed_assertion_line_number = failed_assertion_line_number - 1
    elif 'verifyException("' in all_test_source_code_lines[failed_assertion_line_number - 1]:
        raise Exception(
            f"Found [verifyException()] statement, cannot locate target statement [{test_file_path}][{test_case_name}]")

    related_source_code_lines = []
    for line in all_test_source_code_lines[failed_assertion_line_number - 1::-1]:
        related_source_code_lines.append(line)
        if test_case_method_signature in line:
            break
    related_source_code_lines.reverse()
    related_source_code_lines[0] = TEST_CASE_METHOD_SIGNATURE_TEMPLATE.format(
        test_case_name=test_case_name) + "  {"
    related_source_code_lines[-1] = related_source_code_lines[-1] + " //_X_FAILED_ASSERTION_"
    related_source_code_lines.append("   }")

    # normalize unsupported statements (imported from external libraries such as Evosuite)
    for index, line in enumerate(related_source_code_lines):
        if "mock(" in line and "new ViolatedAssumptionAnswer()" in line:
            left_hand_side = line.split("=", 1)[0]
            variable_type = left_hand_side.strip().rsplit(" ", 1)[0]
            new_right_hand_side = f"new {variable_type}(){{}};"
            normalized_statement = left_hand_side + "= " + new_right_hand_side
            related_source_code_lines[index] = normalized_statement

    purified_test_case_source_code = "\n".join(related_source_code_lines)
    return test_file_path, required_import_statements, purified_test_case_source_code


def get_failed_test_info_from_junit_report(failed_variant_dir):
    junit_report_path = get_junit_report_path(failed_variant_dir)
    failed_test_info_list = []
    test_dir = get_test_dir(failed_variant_dir, force_mkdir=False)

    with open(junit_report_path) as input_file:
        soup = BeautifulSoup(input_file, "html.parser")
        for elm in soup.find_all('tr', {'class': 'Error'}):
            if not str(elm.parent.previous_sibling.previous_sibling.text).startswith("TestCase"):
                continue
            test_file_name = elm.parent.find_previous_sibling("a")["name"].strip() + SOURCE_CODE_EXTENSION

            tr = elm
            td_children = list(tr.findChildren("td", recursive=False))

            test_case_name = td_children[0].text.strip()
            test_case_stack_trace_elm = td_children[2].find("code")
            failed_assertion_line_number = -1
            for code_elm in test_case_stack_trace_elm.children:
                if not isinstance(code_elm, NavigableString):
                    continue
                trace_info = str(code_elm)
                if test_file_name in trace_info:
                    qualified_test_case_class_name = re.search(f"([a-zA-Z._]+).{test_case_name}", trace_info).group(1)
                    test_case_file_path = join_path(test_dir, *qualified_test_case_class_name.split(".")[:-1],
                                                    test_file_name)
                    failed_assertion_line_number = int(
                        re.search(f"{SOURCE_CODE_EXTENSION}:(\d+)\)", trace_info).group(1))
                    break
            failed_test_info_list.append((test_case_file_path, test_case_name, failed_assertion_line_number))
    return failed_test_info_list

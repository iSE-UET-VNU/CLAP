import json
import xml.etree.ElementTree as ET

from FileManager import list_dir, get_slicing_test_case_output_file_path, \
    get_slicing_log_file_path, get_variants_dir, join_path, get_test_coverage_dir, \
    get_failed_spectrum_coverage_file_path_with_version, get_file_name
from suspicious_statements_manager.SuspiciousStatementManager import get_single_buggy_statement, \
    get_multiple_buggy_statements


def get_all_failed_test_case_executed_statements(mutated_project_dir, variant_name):
    variant_dir = join_path(get_variants_dir(mutated_project_dir), variant_name)
    test_coverage_dir = get_test_coverage_dir(variant_dir)
    failed_spectrum_coverage_file_path = get_failed_spectrum_coverage_file_path_with_version(test_coverage_dir)
    tree = ET.parse(failed_spectrum_coverage_file_path)
    root = tree.getroot()
    line_elms = root.findall(".//line[@count]")
    executed_statements = set()
    for line in line_elms:
        if int(line.get("num")) > 0 and int(line.get("count")) > 0:
            feature_line_key = "{}.{}".format(line.get("featureClass"), line.get("featureLineNum"))
            executed_statements.add(feature_line_key)
    return executed_statements


if __name__ == "__main__":
    # ------ START CONFIG ------
    mutants_dir = "/Users/tuanngokien/Desktop/Software_Analysis/configurable_system/dataset/4wise-Email-FH-JML"
    # ------ END CONFIG ------

    mutated_project_dirs = list_dir(mutants_dir, full_path=True)
    print("{} [{} bugs]\n".format(mutants_dir, len(mutated_project_dirs)))
    pts_loss_count = 0
    spc_loss_count = 0

    for mutated_project_dir in mutated_project_dirs:
        mutated_project_name = get_file_name(mutated_project_dir)
        buggy_statements = set(get_multiple_buggy_statements(mutated_project_name, mutated_project_dir))
        slicing_pts_output_file_path = get_slicing_test_case_output_file_path(mutated_project_dir)
        slicing_pts_output_dict = json.load(open(slicing_pts_output_file_path))

        slicing_spc_output_file_path = get_slicing_log_file_path(mutated_project_dir, 0)
        slicing_spc_output_dict = json.load(open(slicing_spc_output_file_path))

        failed_test_cases_executed_statements = set()
        pts_sliced_statements = set()
        spc_sliced_statements = set()

        for variant_name in slicing_pts_output_dict:
            failed_test_cases_executed_statements.update(
                get_all_failed_test_case_executed_statements(mutated_project_dir,
                                                             variant_name))
            pts_sliced_statements.update(slicing_pts_output_dict[variant_name])
            spc_sliced_statements.update(list(slicing_spc_output_dict[variant_name].keys()))

        intersect_statements = pts_sliced_statements & spc_sliced_statements

        if not buggy_statements.issubset(pts_sliced_statements):
            pts_loss_count += 1
        if not buggy_statements.issubset(spc_sliced_statements):
            spc_loss_count += 1

        print(mutated_project_name,
              len(failed_test_cases_executed_statements),
              ("*" if not buggy_statements.issubset(pts_sliced_statements) else "") + str(len(pts_sliced_statements)),
              ("*" if not buggy_statements.issubset(spc_sliced_statements) else "") + str(len(spc_sliced_statements)),
              # ("*" if not buggy_statements.issubset(intersect_statements) else "") + str(len(intersect_statements)),
              sep="\t")

    print("\n------")
    print("PTS_LOSS_COUNT = %d", pts_loss_count)
    print("sPC_LOSS_COUNT = %d", pts_loss_count)
    print("------")

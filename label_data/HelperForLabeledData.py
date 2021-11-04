import csv

from FileManager import *
from label_data.LabelData import *
from FileManager import *
import xml.etree.ElementTree as ET

ACTUAl_PASSING = "AP"
FALSE_PASSING = "FP"
FAILING = "F"
LABELED_FILE_NAME = "variants_testing_label.csv"

VARIANT_NAME = 'VARIANT'
LABEL = 'LABEL'
CREATED_FP = 'FP created from F'
DDU = "DDU"


def get_variants_and_labels(mutated_project_dir):
    variants = {}
    label_file = join_path(mutated_project_dir, LABELED_FILE_NAME)
    with open(label_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            variants[row[VARIANT_NAME]] = {LABEL: row[LABEL], CREATED_FP: row[CREATED_FP]}
    return variants


def write_dict_to_file(file_name, data, fieldnames):
    with open(file_name, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for item in data:
            tmp = {}
            for f in fieldnames:
                if fieldnames.index(f) == 0:
                    tmp[f] = item
                else:
                    tmp[f] = data[item][f]
            writer.writerow(tmp)


def get_stm_ids_per_variant(variant_dir):
    coverage_dir = get_test_coverage_dir(variant_dir)
    spectrum_dirs = [join_path(coverage_dir, SPECTRUM_FAILED_COVERAGE_FILE_NAME),
                     join_path(coverage_dir, SPECTRUM_PASSED_COVERAGE_FILE_NAME)]
    data = {}
    for cfile in spectrum_dirs:
        if os.path.isfile(cfile):
            try:
                tree = ET.parse(cfile)
                root = tree.getroot()
                project = root.find("project")
                for package in project:
                    for file in package:
                        file_name = file.get("path")
                        for line in file:
                            id = line.get('featureClass') + "." + line.get('featureLineNum')
                            key = file_name + "." + line.get('num')
                            if key not in data:
                                data[key] = {}
                                data[key]['id'] = id
                                data[key]['tested'] = 0
                                if int(line.get('count')) != 0:
                                    data[key]['tested'] = 1;
            except:
                logging.info("Exception when parsing %s", cfile)
    return data


def get_all_stm_ids(project_dir):
    system_stm_ids = {}
    variants = get_all_variant_dirs(project_dir)
    for variant in variants:
        variant_name = variant.split("/")[-1]
        system_stm_ids[variant_name] = get_stm_ids_per_variant(variant)
    return system_stm_ids


def read_coverage_file(system_stm_ids, coverage_file_dir):
    data = []
    if os.path.isfile(coverage_file_dir):
        try:
            tree = ET.parse(coverage_file_dir)
            root = tree.getroot()
            project = root.find("project")
            packages = project.findall("package")
            for package in packages:
                files = package.findall("file")
                for file in files:
                    file_path = file.get("path").split("/")
                    src_id = file_path.index("src")
                    file_name = "/".join(file_path[src_id + 1:])
                    lines = file.findall("line")
                    for line in lines:
                        id = file_name + "." + line.get('num')
                        if "count" in line.attrib and int(line.get("count")) > 0:
                            if id in system_stm_ids.keys():
                                if system_stm_ids[id] not in data:
                                    data.append(system_stm_ids[id])
        except:
            logging.info("Exception when parsing %s", coverage_file_dir)
    return data


def get_failings_executions(project_dir, system_stm_ids, failing_variants):
    failed_test_executions = {}
    for variant in failing_variants:
        failed_test_executions[variant] = {}
        variant_dir = get_variant_dir(project_dir, variant)
        failed_tests_coverage_dir = get_failed_test_coverage_dir(variant_dir)
        all_failed_spectrums = list_dir(failed_tests_coverage_dir)
        for file in all_failed_spectrums:
            file_dir = join_path(failed_tests_coverage_dir, file)
            failed_test_executions[variant][file] = read_coverage_file(system_stm_ids[variant], file_dir)
    return failed_test_executions


def get_passing_executions(project_dir, system_stm_ids, variants):
    passed_test_executions = {}
    for variant in variants:
        passed_test_executions[variant] = {}
        variant_dir = get_variant_dir(project_dir, variant)
        passed_tests_coverage_dir = get_passed_test_coverage_dir(variant_dir)
        all_passed_spectrums = list_dir(passed_tests_coverage_dir)
        for file in all_passed_spectrums:
            file_dir = join_path(passed_tests_coverage_dir, file)
            passed_test_executions[variant][file] = read_coverage_file(system_stm_ids[variant], file_dir)
    return passed_test_executions


def get_labeled_failing_variants(project_dir):
    failing_variants = get_failing_variants(project_dir)
    variants_and_labels = get_variants_and_labels(project_dir)
    for item in failing_variants:
        if variants_and_labels[item][LABEL] != FAILING:
            failing_variants.remove(item)
    return failing_variants


def get_stmts_id_in_passing_variants(project_dir, failing_variants):
    passing_variants_stmts = {}
    variants_dir = get_variants_dir(project_dir)
    variants_list = list_dir(variants_dir)
    for variant in variants_list:
        if variant not in failing_variants:
            variant_dir = join_path(variants_dir, variant)
            variant_stmts = get_stm_ids_per_variant(variant_dir)
            passing_variants_stmts[variant] = variant_stmts
    return passing_variants_stmts


def convert_to_dict(passing_variant_stmt):
    stmt_ids = {}
    for item in passing_variant_stmt:
        tmp = passing_variant_stmt[item]

        if tmp["id"] not in stmt_ids:
            stmt_ids[tmp["id"]] = {}
            stmt_ids[tmp["id"]]["tested"] = tmp["tested"]
    return stmt_ids

def similar_path(path1, path2, threshold):
    count = 0
    for item in path1:
        if item in path2:
            count += 1

    if count/len(path1) > threshold:
        return True
    return False


def exist_path(path, list_paths, threshold):
    count = 0
    for p in list_paths:
        if(similar_path(path, list_paths[p], threshold)):
            return True
    return False

def overlap_failed_exection_vs_passing_variant(failing_exections, passing_variant_stmt):
    passing_variant_stmt_dict = convert_to_dict(passing_variant_stmt)
    overlaps = {}
    max = -1000
    for variant_name in failing_exections:
        for test in failing_exections[variant_name]:
            execution = failing_exections[variant_name][test]
            D1 = []
            D2 = []
            for item in execution:
                if item["id"] in passing_variant_stmt_dict:
                    if passing_variant_stmt_dict[item["id"]]["tested"] == 1:
                        D1.append(item["id"])
                    else:
                        D2.append(item["id"])
            overlaps[variant_name + "__" + test] = {"Executed": D1, "Not Executed": D2}
            # overlap_portion_p_executed
            # if(len(D1) + len(D2) > 0):
            #     if len(D1)/(len(D1) + len(D2)) > max:
            #         max = len(D1)/(len(D1) + len(D2))
            # elif max < 0:
            #     max = 1

            # overlap_portion_p_not_executed
            if(len(D1) + len(D2) > 0):
                if len(D2)/(len(D1) + len(D2)) > max:
                    max = len(D2)/(len(D1) + len(D2))
            elif max < 0:
                max = 1

            # #overlap_portion_Si_executed
            # if(len(execution) > 0):
            #     if len(D1)/len(execution) > max:
            #         max = len(D1)/len(execution)
            # elif max < 0:
            #     max = 0

            # #overlap_portion_Si_not_executed
            # if (len(execution) > 0):
            #     if len(D2) / len(execution) > max:
            #         max = len(D2) / len(execution)
            # elif max < 0:
            #     max = 0
    #return overlaps
    return max
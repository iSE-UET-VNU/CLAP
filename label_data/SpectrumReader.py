import logging
import os

from FileManager import join_path, list_dir, get_failed_test_coverage_dir, get_variant_dir, get_test_coverage_dir, \
    SPECTRUM_FAILED_COVERAGE_FILE_NAME, SPECTRUM_PASSED_COVERAGE_FILE_NAME, get_all_variant_dirs, \
    get_passed_test_coverage_dir
import xml.etree.ElementTree as ET

def get_all_stm_ids(project_dir):
    system_stm_ids = {}
    variants = get_all_variant_dirs(project_dir)
    for variant in variants:
        variant_name = variant.split("/")[-1]
        system_stm_ids[variant_name] = get_stm_ids_per_variant(variant)
    return system_stm_ids

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


def similar_path(path1, path2, threshold):
    count = 0
    for item in path1:
        if item in path2:
            count += 1
    if len(path1) != 0 and count / len(path1) > threshold:
        return True
    return False
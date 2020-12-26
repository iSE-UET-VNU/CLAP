import logging
import os
from os.path import isfile

from FileManager import join_path, SLICING_LOG_FILE_NAME, get_slicing_log_file_path, get_variants_dir, get_variant_dir, \
    get_test_coverage_dir, SPECTRUM_FAILED_COVERAGE_FILE_NAME
import json
import xml.etree.ElementTree as ET

def get_suspicious_statement(mutated_project_dir, filtering_coverage_rate):
    slicing_info_file_path = get_slicing_log_file_path(mutated_project_dir, filtering_coverage_rate)
    failing_coverage_data = read_coverage_file(mutated_project_dir)
    if (isfile(slicing_info_file_path)):
        slicing_info_file = open(slicing_info_file_path, "r")
        slicing_info_content = slicing_info_file.readline()

        suspicious_stms_list = json.loads(slicing_info_content)
        slicing_info_file.close()
        for key in suspicious_stms_list:

            suspicious_temp = []
            for stm in suspicious_stms_list[key].keys():
                if stm not in failing_coverage_data[key]:
                    suspicious_temp.append(stm)

            for stm in suspicious_temp:
                suspicious_stms_list[key].pop(stm)

        return suspicious_stms_list
    else:
        return {}

def read_coverage_file(mutated_project_dir):
    variants_dir = get_variants_dir(mutated_project_dir)
    variants_list = os.listdir(variants_dir)
    data = {}
    for variant in variants_list:
        variant_dir = get_variant_dir(mutated_project_dir, variant)
        test_coverage_dir = get_test_coverage_dir(variant_dir)

        coverage_file = join_path(test_coverage_dir, SPECTRUM_FAILED_COVERAGE_FILE_NAME)
        if os.path.isfile(coverage_file):
            data[variant] = []
            try:
                tree = ET.parse(coverage_file)
                root = tree.getroot()
                project = root.find("project")

                for package in project:
                    for file in package:
                        for line in file:
                            id = line.get('featureClass') + "." + line.get('featureLineNum')
                            if id not in data[variant] and int(line.get('count')) != 0:

                                data[variant].append(id)
            except:
                logging.info("Exception when parsing %s", coverage_file)
    return data

def get_buggy_statement(mutated_project_name, mutated_project_dir):
    mutated_log_file_path = join_path(mutated_project_dir, mutated_project_name + ".mutant.log")
    mutated_log_file = open(mutated_log_file_path, "r")
    mutated_log_file_content = mutated_log_file.readline().split(":")
    buggy_line_number_position_in_log_file = 1
    return (".").join(mutated_project_name.split(".")[0:-1]) + "." + mutated_log_file_content[
        buggy_line_number_position_in_log_file]

def get_single_buggy_statement(mutated_project_name, mutated_project_dir):
    mutated_log_file_path = join_path(mutated_project_dir, mutated_project_name + ".mutant.log")
    mutated_log_file = open(mutated_log_file_path, "r")
    bug_content = mutated_log_file.readline().split(":")
    buggy_line_number_position_in_log_file = 1
    buggy_statement = (".").join(bug_content[0].split(".")[0:-1]) + "." + bug_content[buggy_line_number_position_in_log_file]

    return buggy_statement

def get_mutation_operator(mutated_project_name, mutated_project_dir):
    mutated_log_file_path = join_path(mutated_project_dir, mutated_project_name + ".mutant.log")
    mutated_log_file = open(mutated_log_file_path, "r")
    mutated_log_file_content = mutated_log_file.readline().split(":")
    return  mutated_log_file_content[0]

def get_single_mutation_operator(mutated_project_name, mutated_project_dir):
    mutated_log_file_path = join_path(mutated_project_dir, mutated_project_name + ".mutant.log")
    mutated_log_file = open(mutated_log_file_path, "r")
    bug_content = mutated_log_file.readline().split(":")
    return bug_content[0]


def get_multiple_buggy_statements(mutated_project_name, mutated_project_dir):
    mutated_log_file_path = join_path(mutated_project_dir, mutated_project_name + ".mutant.log")
    mutated_log_file = open(mutated_log_file_path, "r")
    bugs_content = mutated_log_file.readlines()
    buggy_line_number_position_in_log_file = 1
    buggy_statements = []
    for item in bugs_content:
        contents = item.split(":")
        buggy_statements.append((".").join(contents[0].split(".")[0:-1]) + "." + contents[buggy_line_number_position_in_log_file])
    return buggy_statements
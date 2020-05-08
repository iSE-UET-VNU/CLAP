from os.path import isfile

from FileManager import join_path, SLICING_LOG_FILE_NAME
import json

def get_suspicious_statement(mutated_project_dir):
    slicing_info_file_path = join_path(mutated_project_dir, SLICING_LOG_FILE_NAME)

    if(isfile(slicing_info_file_path)):
        slicing_info_file = open(slicing_info_file_path, "r")
        slicing_info_content = slicing_info_file.readline()

        suspicious_stms_list = json.loads(slicing_info_content)
        slicing_info_file.close()
        return suspicious_stms_list
    else:
        return {}

def get_buggy_statement(mutated_project_name, mutated_project_dir):
    mutated_log_file_path = join_path(mutated_project_dir, mutated_project_name + ".mutant.log")
    mutated_log_file = open(mutated_log_file_path, "r")
    mutated_log_file_content = mutated_log_file.readline().split(":")
    buggy_line_number_position_in_log_file = 1
    return (".").join(mutated_project_name.split(".")[0:-1]) + "." + mutated_log_file_content[buggy_line_number_position_in_log_file]

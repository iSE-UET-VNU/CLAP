import csv

import AntManager
import ConfigManager
import TestManager
import VariantComposer
from FileManager import get_all_variant_dirs, get_model_configs_report_path, get_file_name, get_file_name_without_ext, \
    get_outer_dir, join_path, get_dependency_lib_dirs, is_path_exist, delete_dir, touch_file, \
    get_variant_dir_from_config_path


def find_involving_feature(project_dir, mutated_project_dir):
    failed_variant_dir_items = get_failed_variant_dir_items(mutated_project_dir)
    for item in failed_variant_dir_items:
        failed_variant_name, failed_variant_dir = item
        related_config_path = get_related_config_path(failed_variant_name, project_dir)
        switched_config_paths = compose_switched_configs(related_config_path, failed_variant_name)
        compose_switched_products(switched_config_paths, project_dir, mutated_project_dir)


def get_failed_variant_dir_items(mutated_project_dir):
    variant_dirs = get_all_variant_dirs(mutated_project_dir, sort=True)
    configs_report_file_path = get_model_configs_report_path(mutated_project_dir)
    failed_variant_dir_items = []
    with open(configs_report_file_path, "r") as report_csv:
        reader = csv.reader(report_csv)
        next(reader)
        for i, row in enumerate(reader):
            test_passed = row[-1] == "__PASSED__"
            if not test_passed:
                failed_variant_name = row[0]
                for d in variant_dirs:
                    split_variant_name = get_file_name(d)
                    if split_variant_name == failed_variant_name:
                        failed_variant_dir_items.append((failed_variant_name, d))
    return failed_variant_dir_items


def get_related_config_path(variant_name, project_dir):
    config_paths = ConfigManager.get_config_paths(project_dir, sort=True)
    for p in config_paths:
        split_config_name = get_file_name_without_ext(p)
        if split_config_name == variant_name:
            return p


def compose_switched_configs(config_path, variant_name):
    feature_selections = get_feature_selections(config_path)
    switched_feature_selections_container = get_single_switched_feature_selections(feature_selections)
    configs_dir = get_outer_dir(config_path)
    switched_config_path_container = []
    for i, fs in enumerate(switched_feature_selections_container):
        switched_config_file_name = f"{variant_name}_SW{i + 1}.features"
        switched_config_file_path = join_path(configs_dir, switched_config_file_name)
        if not is_path_exist(switched_config_file_path):
            with open(switched_config_file_path, "w+") as output_file:
                for f_index, name in enumerate(fs):
                    line = name if fs[name] else f"#{name}"
                    if f_index < len(fs) - 1:
                        line += "\n"
                    output_file.write(line)
        switched_config_path_container.append(switched_config_file_path)
    return switched_config_path_container


def get_single_switched_feature_selections(feature_selections):
    feature_selections_container = []
    for name, status in feature_selections.items():
        switched_status = not status
        switched_feature_selections = dict(feature_selections)
        switched_feature_selections[name] = switched_status
        feature_selections_container.append(switched_feature_selections)
    return feature_selections_container


def get_feature_selections(config_path):
    feature_selections = {}
    with open(config_path) as input_file:
        for line in input_file:
            line = line.strip()
            if line:
                if line.startswith("#"):
                    feature_name = line[1:]
                    status = False
                else:
                    feature_name = line
                    status = True
                feature_selections[feature_name] = status
    return feature_selections


def compose_switched_products(config_paths, project_dir, mutated_project_dir):
    cloned_ant_name = AntManager.clone_ant_plugin()
    lib_paths = get_dependency_lib_dirs(project_dir)
    for config_path in config_paths:
        variant_dir = get_variant_dir_from_config_path(project_dir, config_path)
        corrupt_file = join_path(variant_dir, "corrupted_compile.log")
        if not is_path_exist(variant_dir):
            variant_dir = VariantComposer.compose_by_config(project_dir, config_path)
            compile_log = AntManager.compile_source_classes(lib_paths=lib_paths, variant_dir=variant_dir)
            if compile_log.find("BUILD SUCCESSFUL") < 0:
                print("********\n__FAILED__", config_path, "\n********\n")
                touch_file(corrupt_file)
                # delete_dir(variant_dir)
                continue
            TestManager.generate_junit_test_cases(lib_paths=lib_paths, variant_dir=variant_dir)
            TestManager.run_batch_junit_test_cases(variant_dir, lib_paths=lib_paths, halt_on_failure=True,
                                                   halt_on_error=True, custom_ant=cloned_ant_name)
        elif is_path_exist(corrupt_file):
            print("********\n\n__SKIP__FAILED__", config_path, "\n********\n")
            continue
        # mutated_variant_dir = VariantComposer.compose_by_config(mutated_project_dir, config_path)
        # TestManager.link_generated_junit_test_cases(variant_dir, mutated_variant_dir)
        # is_all_test_passed = TestManager.run_batch_junit_test_cases(mutated_variant_dir, lib_paths=lib_paths,
        #                                                             halt_on_failure=False,
        #                                                             halt_on_error=True, custom_ant=cloned_ant_name)
        # if is_all_test_passed:
        #     file_name = "sw.test.passed.txt"
        # else:
        #     file_name = "sw.test.failed.txt"
        # test_flag_file = join_path(mutated_variant_dir, file_name)
        # touch_file(test_flag_file)

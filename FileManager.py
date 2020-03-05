import os
import shutil
from pathlib import Path

PLUGIN_DIR = os.path.abspath("plugins")
PROJECT_DIR = os.path.abspath("projects")
MODE_FILE_NAME = "model.m"
CONFIG_FOLDER_NAME = "configs"
VARIANT_FOLDER_NAME = "variants"
FEATURE_FOLDER_NAME = "features"


def mkdir_if_not_exist(input_dir):
    if not os.path.exists(input_dir):
        os.makedirs(input_dir)


def get_plugin_path(file_name):
    return os.path.join(PLUGIN_DIR, file_name)


def get_model_file_path(project_dir):
    model_file_path = os.path.join(project_dir, MODE_FILE_NAME)
    if not os.path.isfile(model_file_path):
        raise FileNotFoundError(f"Can't find model file from [{model_file_path}]")
    return model_file_path


def get_project_dir(project_name):
    return os.path.join(PROJECT_DIR, project_name)


def get_model_config_dir(project_dir):
    config_dir = os.path.join(project_dir, CONFIG_FOLDER_NAME)
    mkdir_if_not_exist(config_dir)
    return config_dir


def get_variant_dir(project_dir, config_name):
    variant_dir = os.path.join(project_dir, VARIANT_FOLDER_NAME, config_name)
    mkdir_if_not_exist(variant_dir)
    return variant_dir


def get_feature_source_code_dir(project_dir):
    feature_dir = os.path.join(project_dir, FEATURE_FOLDER_NAME)
    mkdir_if_not_exist(feature_dir)
    return feature_dir


def get_outer_dir(current_path, step=1):
    current_dir = Path(current_path)
    for _ in range(step):
        current_dir = current_dir.parent
    return current_dir


def move_file(source, target):
    shutil.move(source, target)


def split_path(file_path):
    return file_path.rsplit("/", 1)


def get_file_name(file_path):
    return os.path.basename(file_path).rsplit(".", 1)[0]


def join_path(path1, path2):
    return os.path.join(path1, path2)


def is_path_exist(path):
    return os.path.exists(path)

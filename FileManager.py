import os
import re
import shutil
from pathlib import Path

PLUGIN_DIR = os.path.abspath("plugins")

PROJECT_DIR = os.path.abspath("projects")

MODE_FILE_NAME = "model.m"
CONFIG_FOLDER_NAME = "configs"

VARIANT_FOLDER_NAME = "variants"
FEATURE_FOLDER_NAME = "features"

MUTATION_RESULT_FOLDER_NAME = "mutation_result"
MUTATED_PROJECTS_FOLDER_NAME = "mutated_projects"


def mkdir_if_not_exist(input_dir):
    if not is_path_exist(input_dir):
        os.makedirs(input_dir)


def get_plugin_path(file_name):
    return join_path(PLUGIN_DIR, file_name)


def get_model_file_path(project_dir):
    model_file_path = join_path(project_dir, MODE_FILE_NAME)
    if not is_path_exist(model_file_path):
        raise FileNotFoundError(f"Can't find model file from [{model_file_path}]")
    return model_file_path


def get_project_dir(project_name):
    return get_absolute_path(join_path(PROJECT_DIR, project_name))


def get_project_sub_dir_by_folder_name(project_dir, *args, **kwargs):
    sub_dir = join_path(project_dir, *args, **kwargs)
    mkdir_if_not_exist(sub_dir)
    return sub_dir


def get_model_config_dir(project_dir):
    return get_project_sub_dir_by_folder_name(project_dir, CONFIG_FOLDER_NAME)


def get_variant_dir(project_dir, config_name):
    return get_project_sub_dir_by_folder_name(project_dir, VARIANT_FOLDER_NAME, config_name)


def get_mutation_result_dir(project_dir):
    return get_project_sub_dir_by_folder_name(project_dir, MUTATION_RESULT_FOLDER_NAME)


def get_mutated_projects_dir(project_dir):
    return get_project_sub_dir_by_folder_name(project_dir, MUTATED_PROJECTS_FOLDER_NAME)


def get_feature_source_code_dir(project_dir):
    return get_project_sub_dir_by_folder_name(project_dir, FEATURE_FOLDER_NAME)


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


def join_path(*args, **kwargs):
    return os.path.join(*args, **kwargs)


def is_path_exist(path):
    return os.path.exists(path)


def is_symlink(path):
    return os.path.islink(path)


def get_absolute_path(current_path):
    return os.path.abspath(current_path)


def list_dir(current_dir):
    return filter(lambda d: not d.startswith("."), os.listdir(current_dir))


def delete_dir(directory):
    directory = Path(directory)
    for item in directory.iterdir():
        if item.is_dir():
            delete_dir(item)
        else:
            item.unlink()
    directory.rmdir()


def escape_path(current_path):
    return os.path.normpath(re.sub(r'(?=[()])', r'\\', current_path))


def create_symlink(src, dst):
    if is_path_exist(dst):
        os.unlink(dst)
    os.symlink(src, escape_path(dst))


def copy_dir(src, dst):
    if is_path_exist(dst):
        delete_dir(dst)
    shutil.copytree(src, dst)

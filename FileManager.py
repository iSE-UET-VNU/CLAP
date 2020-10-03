import os
import re
import shutil
from pathlib import Path

from Helpers import get_logger

PLUGIN_DIR = os.path.abspath("plugins")
LOG_DIR = os.path.abspath("logs")
PROJECT_DIR = os.path.abspath("projects")

MODE_FILE_NAME = "model.m"
FEATURE_ORDER_FILE_NAME = "features.order"
LIB_FOLDER_NAME = "lib"
CONFIG_FOLDER_NAME = "configs"
CONFIGS_REPORT_FILE_NAME = "config.report.csv"
SPC_LOG_FILE_NAME = "spc_{}.log"
SLICING_LOG_FILE_NAME = "slicing_{}.log"
PROJECT_LOCK_FILE_NAME = "project.lock"

VARIANT_FOLDER_NAME = "variants"
SRC_FOLDER_NAME = "src"
TEST_FOLDER_NAME = "test"
COMPILED_CLASSES_FOLDER_NAME = "build"
COMPILED_SOURCE_CLASSES_FOLDER_NAME = "main"
COMPILED_TEST_CLASSES_FOLDER_NAME = "test"
TEST_RESULTS_FOLDER_NAME = "test_results"
COVERAGE_FOLDER_NAME = "coverage"
TEST_CASES_FOLDER_NAME = "test"
FEATURE_FOLDER_NAME = "features"

MUTATION_RESULT_FOLDER_NAME = "mutation_result"
MUTATED_PROJECTS_FOLDER_NAME = "mutated_projects"

SPECTRUM_FAILED_COVERAGE_FILE_NAME = "spectrum_failed_coverage.xml"
SPECTRUM_PASSED_COVERAGE_FILE_NAME = "spectrum_passed_coverage.xml"
FAILED_TEST_COVERAGE_FOLDER_NAME = "failed"
PASSED_TEST_COVERAGE_FOLDER_NAME = "passed"

EXPERIMENT_RESULT_FOLDER = os.path.abspath("experiment_results")
RUNTIME_LOG_FOLDER = os.path.abspath("runtime_logs")

logger = get_logger(__name__)


def mkdir_if_not_exist(input_dir):
    if not is_path_exist(input_dir):
        os.makedirs(input_dir)

def get_experimetal_result_system_dir(system_name):
    return join_path(EXPERIMENT_RESULT_FOLDER, system_name)

def get_experimetal_result_k_wise(system_dir, k_wise):
    return join_path(system_dir, k_wise)

def get_experimental_result_file(k_wise_dir, file_name):
    return join_path(k_wise_dir, file_name)


def get_plugin_path(file_name):
    return join_path(PLUGIN_DIR, file_name)


def get_log_file_path(file_name):
    return join_path(get_project_sub_dir_by_folder_name(LOG_DIR), file_name)


def get_model_file_path(project_dir):
    model_file_path = join_path(project_dir, MODE_FILE_NAME)
    if not is_path_exist(model_file_path):
        raise FileNotFoundError(f"Can't find model file from [{model_file_path}]")
    return model_file_path


def get_feature_order_file_path(project_dir):
    feature_order_file_path = join_path(project_dir, FEATURE_ORDER_FILE_NAME)
    return feature_order_file_path


def get_project_dir(project_name, base_dir=None):
    if not base_dir:
        return join_path(PROJECT_DIR, project_name)
    else:
        return join_path(base_dir, project_name)


def get_project_name(project_dir):
    return get_file_name(project_dir)


def get_project_sub_dir_by_folder_name(project_dir, *args, **kwargs):
    force_mkdir = kwargs.pop("force_mkdir", True)
    sub_dir = join_path(project_dir, *args, **kwargs)
    if force_mkdir:
        mkdir_if_not_exist(sub_dir)
    return sub_dir


def get_model_configs_dir(project_dir):
    return get_project_sub_dir_by_folder_name(project_dir, CONFIG_FOLDER_NAME)


def get_model_configs_report_path(project_dir):
    return join_path(project_dir, CONFIGS_REPORT_FILE_NAME)


def get_dependency_lib_dirs(project_dir):
    libs_dir = get_project_sub_dir_by_folder_name(project_dir, LIB_FOLDER_NAME)
    return list_dir(libs_dir, full_path=True)


def get_variants_dir(project_dir):
    return get_project_sub_dir_by_folder_name(project_dir, VARIANT_FOLDER_NAME)


def get_all_variants_dirs(project_dir):
    variants_dir = get_variants_dir(project_dir)
    return list_dir(variants_dir, full_path=True)


def get_spc_log_file_path(project_dir, filtering_coverage_rate):
    return join_path(project_dir, SPC_LOG_FILE_NAME.format(int(filtering_coverage_rate * 100)))


def get_slicing_log_file_path(project_dir, filtering_coverage_rate):
    return join_path(project_dir, SLICING_LOG_FILE_NAME.format(int(filtering_coverage_rate * 100)))


def get_variant_dir(project_dir, config_name):
    return get_project_sub_dir_by_folder_name(get_variants_dir(project_dir), config_name)


def get_compiled_classes_dir(variant_dir):
    return get_project_sub_dir_by_folder_name(variant_dir, COMPILED_CLASSES_FOLDER_NAME)


def get_compiled_source_classes_dir(variant_dir):
    return get_project_sub_dir_by_folder_name(get_compiled_classes_dir(variant_dir),
                                              COMPILED_SOURCE_CLASSES_FOLDER_NAME)


def get_compiled_test_classes_dir(variant_dir):
    return get_project_sub_dir_by_folder_name(get_compiled_classes_dir(variant_dir),
                                              COMPILED_TEST_CLASSES_FOLDER_NAME, force_mkdir=False)


def get_test_results_dir(variant_dir):
    return get_project_sub_dir_by_folder_name(get_compiled_classes_dir(variant_dir),
                                              TEST_RESULTS_FOLDER_NAME, force_mkdir=False)


def get_test_coverage_dir(variant_dir):
    return get_project_sub_dir_by_folder_name(variant_dir, COVERAGE_FOLDER_NAME, force_mkdir=False)


def get_src_dir(variant_dir):
    return get_project_sub_dir_by_folder_name(variant_dir, SRC_FOLDER_NAME, force_mkdir=False)


def get_test_dir(variant_dir, force_mkdir=True):
    return get_project_sub_dir_by_folder_name(variant_dir, TEST_FOLDER_NAME, force_mkdir=force_mkdir)


def get_mutation_result_dir(project_dir):
    return get_project_sub_dir_by_folder_name(project_dir, MUTATION_RESULT_FOLDER_NAME)


def get_mutated_projects_dir(project_dir):
    return get_project_sub_dir_by_folder_name(project_dir, MUTATED_PROJECTS_FOLDER_NAME)


def get_feature_source_code_dir(project_dir):
    return get_project_sub_dir_by_folder_name(project_dir, FEATURE_FOLDER_NAME)


def get_implemented_features(project_dir):
    features_dir = get_feature_source_code_dir(project_dir)
    implemented_features = list_dir(features_dir)
    return implemented_features


def get_passed_spectrum_coverage_file_path_with_version(variant_dir, version=""):
    return get_spectrum_coverage_file_path_with_version(variant_dir, SPECTRUM_PASSED_COVERAGE_FILE_NAME, version)


def get_failed_spectrum_coverage_file_path_with_version(variant_dir, version=""):
    return get_spectrum_coverage_file_path_with_version(variant_dir, SPECTRUM_FAILED_COVERAGE_FILE_NAME, version)


def get_spectrum_coverage_file_path_with_version(variant_dir, original_coverage_file_name, version=""):
    if version:
        version = version + "__"
    return join_path(get_test_coverage_dir(variant_dir), version + original_coverage_file_name)


def is_project_locked(project_dir):
    lock_file_path = join_path(project_dir, PROJECT_LOCK_FILE_NAME)
    return is_path_exist(lock_file_path)


def lock_project(project_dir):
    if not is_project_locked(project_dir):
        lock_file_path = join_path(project_dir, PROJECT_LOCK_FILE_NAME)
        touch_file(lock_file_path)
        logger.info(f"Project [{get_file_name(project_dir)}] has been locked successfully")
    else:
        message = f"Project [{get_file_name(project_dir)}] had been locked by another process, try again later"
        logger.error(message)
        raise BlockingIOError(message)


def get_outer_dir(current_path, step=1):
    current_dir = Path(current_path)
    for _ in range(step):
        current_dir = current_dir.parent
    return current_dir


def move_file(source, target):
    shutil.move(source, target)


def split_path(file_path):
    return file_path.rsplit(os.sep, 1)


def get_file_name_without_ext(file_path):
    return get_file_name(file_path).rsplit(".", 1)[0]


def get_file_name(file_path):
    return os.path.basename(file_path)


def get_file_name_with_parent(file_path):
    return join_path(*file_path.rsplit(os.sep, 2)[1:])


def join_path(*args, **kwargs):
    return os.path.join(*args, **kwargs)


def is_path_exist(path):
    return os.path.exists(path)


def is_symlink(path):
    return os.path.islink(path)


def get_absolute_path(current_path):
    return os.path.abspath(current_path)


def list_dir(current_dir, full_path=False):
    files = list(filter(lambda d: not d.startswith("."), os.listdir(current_dir)))
    if full_path:
        files = [join_path(current_dir, file) for file in files]
    return files


def delete_dir(directory):
    directory = Path(directory)
    if not directory.is_dir():
        return
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
        try:
            os.unlink(dst)
        except (IsADirectoryError, PermissionError):
            pass
    else:
        mkdir_if_not_exist(get_outer_dir(dst))
    os.symlink(src, escape_path(dst))


def create_non_hidden_file_symlink(src, dst):
    if is_path_exist(dst):
        os.unlink(dst)
    mkdir_if_not_exist(dst)
    for file in list_dir(src):
        if file.startswith("."):
            continue
        current_src = join_path(src, file)
        current_dst = join_path(dst, file)
        create_symlink(current_src, current_dst)


def remove_file(file_path):
    os.remove(file_path)


def copy_file(src, dst):
    if is_path_exist(dst):
        delete_dir(dst)
    shutil.copyfile(src, dst)


def copy_dir(src, dst):
    if is_path_exist(dst):
        delete_dir(dst)
    shutil.copytree(src, dst)


def touch_file(file_path):
    Path(file_path).touch()

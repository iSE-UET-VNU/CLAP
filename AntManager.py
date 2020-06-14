from FileManager import get_plugin_path, get_file_name_without_ext, get_src_dir, get_compiled_source_classes_dir, \
    get_test_dir, get_compiled_test_classes_dir, create_non_hidden_file_symlink, get_file_name
from Helpers import get_logger, execute_shell_command, get_current_timestamp
from TestManager import EVOSUITE_PLUGIN_PATH

logger = get_logger(__name__)

SHELL_BUILDER_PLUGIN_NAME = "java_builder.sh"
SHELL_BUILDER_PLUGIN_PATH = get_plugin_path(SHELL_BUILDER_PLUGIN_NAME)

ANT_PLUGIN_NAME = "apache-ant-1.10.7"
ANT_PLUGIN_PATH = get_plugin_path(ANT_PLUGIN_NAME)


def compile_source_classes(lib_paths, variant_dir):
    logger.info(f"Compiling source code [{get_file_name_without_ext(variant_dir)}] ")
    source_dir = get_src_dir(variant_dir)
    source_classes_dir = get_compiled_source_classes_dir(variant_dir)
    return compile_classes(source_dir, source_classes_dir, lib_path=lib_paths)


def compile_test_classes(variant_dir):
    logger.info(f"Compiling test cases [{get_file_name_without_ext(variant_dir)}] ")
    test_src_dir = get_test_dir(variant_dir)
    test_classes_dir = get_compiled_test_classes_dir(variant_dir)
    source_classes_dir = get_compiled_source_classes_dir(variant_dir)
    return compile_classes(test_src_dir, test_classes_dir, lib_path=[source_classes_dir, EVOSUITE_PLUGIN_PATH])


def compile_classes(src, out, lib_path=None):
    if lib_path is None:
        lib_path = []
    joined_lib_path = ":".join(lib_path)

    output_log = execute_shell_command(f'/bin/sh {SHELL_BUILDER_PLUGIN_PATH}', extra_args=[
        {"-src": src},
        {"-out": out},
        {"-classpath": joined_lib_path},
    ])
    if output_log.find("BUILD SUCCESSFUL") < 0:
        logger.fatal(f"{output_log}\n\nFailed to compile source code [{src}]")
    return output_log


def clone_ant_plugin():
    cloned_ant_plugin_path = "{}.cloned.{}".format(ANT_PLUGIN_PATH, get_current_timestamp())
    create_non_hidden_file_symlink(ANT_PLUGIN_PATH, cloned_ant_plugin_path)
    return get_file_name(cloned_ant_plugin_path)

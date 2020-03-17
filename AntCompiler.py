from FileManager import get_plugin_path, get_file_name, get_src_dir, get_compiled_source_classes_dir, get_test_dir, \
    get_compiled_test_classes_dir
from Helpers import get_logger, execute_shell_command
from TestManager import EVOSUITE_PLUGIN_PATH

logger = get_logger(__name__)

PLUGIN_NAME = "java_builder.sh"
PLUGIN_PATH = get_plugin_path(PLUGIN_NAME)


def compile_source_classes(variant_dir):
    logger.info(f"Compiling source code [{get_file_name(variant_dir)}] ")
    source_dir = get_src_dir(variant_dir)
    source_classes_dir = get_compiled_source_classes_dir(variant_dir)
    return compile_classes(source_dir, source_classes_dir)


def compile_test_classes(variant_dir):
    logger.info(f"Compiling test cases [{get_file_name(variant_dir)}] ")
    test_src_dir = get_test_dir(variant_dir)
    test_classes_dir = get_compiled_test_classes_dir(variant_dir)
    source_classes_dir = get_compiled_source_classes_dir(variant_dir)
    return compile_classes(test_src_dir, test_classes_dir, class_path=[source_classes_dir, EVOSUITE_PLUGIN_PATH])


def compile_classes(src, out, class_path=None):
    if class_path is None:
        class_path = []
    joined_class_path = ":".join(class_path)

    output_log = execute_shell_command(f'/bin/sh {PLUGIN_PATH}', extra_args=[
        {"-src": src},
        {"-out": out},
        {"-classpath": joined_class_path},
    ])
    if not output_log.find("BUILD SUCCESSFUL"):
        logger.fatal(f"{output_log}\n\nFailed to compile source code [{src}]")
    return output_log

from FileManager import get_plugin_path, split_path, join_path
from Helpers import get_logger, execute_shell_command

logger = get_logger(__name__)

PLUGIN_NAME = "muJava.jar"
PLUGIN_PATH = get_plugin_path(PLUGIN_NAME)
MUTATED_FEATURES_FOLDER_NAME = "mutation_result"


def assign_current_project_as_new_session(current_project_dir):
    projects_dir, project_name = split_path(current_project_dir)
    execute_shell_command(f'java -Dmujava_home={projects_dir} -cp {PLUGIN_PATH} mujava.cli.testnew', extra_args=[
        {project_name: ""},
    ])


def make_mutants(current_project_dir):
    projects_dir, project_name = split_path(current_project_dir)
    execute_shell_command(f'java -Dmujava_home={projects_dir} -cp {PLUGIN_PATH} mujava.cli.genmutes',
                          extra_args=[
                              {"-all": ""},
                              {project_name: ""},
                          ])
    mutation_result_dir = join_path(current_project_dir, MUTATED_FEATURES_FOLDER_NAME)
    return mutation_result_dir


def generate(project_dir):
    logger.info(f"Mutating features [{project_dir}]")
    assign_current_project_as_new_session(project_dir)
    return make_mutants(project_dir)

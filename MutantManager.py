import csv

from FileManager import get_plugin_path, split_path, get_mutation_result_dir, list_dir, join_path, \
    get_mutated_projects_dir, create_symlink, get_feature_source_code_dir, get_file_name_without_ext, copy_dir, \
    is_path_exist, get_model_configs_report_path, get_project_name
from Helpers import get_logger, execute_shell_command

logger = get_logger(__name__)

PLUGIN_NAME = "muJava.jar"
PLUGIN_PATH = get_plugin_path(PLUGIN_NAME)


def assign_current_project_as_new_session(current_project_dir):
    projects_dir, project_name = split_path(current_project_dir)
    execute_shell_command(f'java -Dmujava_home={projects_dir} -cp {PLUGIN_PATH} mujava.cli.testnew', extra_args=[
        {project_name: ""},
    ])


def get_all_mutant_paths(mutation_result_dir):
    """
        Mutation result tracing path for each mutated operator
            mutation_result -> feature_class (eg. Base.GPL.EdgeIter)
            -> traditional_mutants -> mutated method (eg. boolean_hasNext())
            -> mutation operators (eg. SDL_1) -> mutated class file (eg. EdgeIter.java)
        """

    output = execute_shell_command(f"find {mutation_result_dir}",
                                   extra_args=[
                                       {"-mindepth": 4},
                                       {"-type": "f"},
                                       {"-name": "\"*.java\""},
                                   ])
    return output.split("\n")[:-1]


def count_mutants(mutant_paths):
    return len(mutant_paths)


def make_mutants(current_project_dir, optional_feature_names):
    projects_dir, project_name = split_path(current_project_dir)
    execute_shell_command(
        f'java -Dmujava_home={projects_dir} -Dallowed_features={",".join(optional_feature_names)} -cp {PLUGIN_PATH} mujava.cli.genmutes',
        extra_args=[
            {"-all": ""},
            {project_name: ""},
        ])
    mutation_result_dir = get_mutation_result_dir(current_project_dir)
    mutant_paths = get_all_mutant_paths(mutation_result_dir)
    mutant_count = count_mutants(mutant_paths)
    logger.info(f"Composed {mutant_count} mutants [{get_file_name_without_ext(mutation_result_dir)}]")
    return mutant_paths


def generate_mutants(project_dir, optional_feature_names):
    logger.info(f"Mutating features [{get_file_name_without_ext(project_dir)}]")
    assign_current_project_as_new_session(project_dir)
    mutant_paths = make_mutants(project_dir, optional_feature_names)
    mutated_project_dirs = inject_mutants(project_dir, mutant_paths)
    return mutated_project_dirs


def inject_mutants(project_dir, mutant_paths):
    logger.info(f"Injecting mutants to features [{get_file_name_without_ext(project_dir)}]")
    mutated_projects_dir = get_mutated_projects_dir(project_dir)
    features_dir = get_feature_source_code_dir(project_dir)
    mutated_project_dirs = []
    for mutant_path in mutant_paths:
        # FORMAT: ~/InputPreparation/projects/GPL-Test/mutation_result/DirectedWithEdges.GPL.Edge/traditional_mutants/Vertex_getOtherVertex(Vertex)/ROR_1/Edge.java'
        mutant_path_parts = mutant_path.rsplit("/", 5)
        full_class_name = mutant_path_parts[1]
        package, class_name = full_class_name.rsplit(".", 1)
        class_name += ".java"
        operator_index = mutant_path_parts[4]
        current_project_name = f"{full_class_name}.{operator_index}"

        current_mutated_project_dir = join_path(mutated_projects_dir, current_project_name)
        current_mutated_features_dir = get_feature_source_code_dir(project_dir=current_mutated_project_dir)

        mutation_log_file = join_path(*mutant_path_parts[:-3], "mutation_logs", f"{current_project_name}.log")
        mutated_project_mutation_log_file = join_path(current_mutated_project_dir, f"{current_project_name}.mutant.log")
        create_symlink(mutation_log_file, mutated_project_mutation_log_file)

        for feature_name in list_dir(features_dir):
            current_feature_dir = join_path(features_dir, feature_name)
            current_mutated_feature_dir = join_path(current_mutated_features_dir, feature_name)

            if feature_name == package.split(".")[0]:
                copy_dir(current_feature_dir, current_mutated_feature_dir)
            else:
                create_symlink(current_feature_dir, current_mutated_feature_dir)

        mutant_path_dst = join_path(current_mutated_features_dir, *package.split("."), class_name)
        create_symlink(mutant_path, mutant_path_dst)

        mutated_project_dirs.append(current_mutated_project_dir)
    return mutated_project_dirs


def get_mutated_project_dirs(project_dir):
    mutated_projects_dir = get_mutated_projects_dir(project_dir)
    return list_dir(mutated_projects_dir, full_path=True)


def get_mutated_project_dir(project_dir, mutated_project_name):
    mutated_projects_dir = get_mutated_projects_dir(project_dir)
    current_mutated_project_dir = join_path(mutated_projects_dir, mutated_project_name)
    if not is_path_exist(current_mutated_project_dir):
        logger.fatal("Can't find mutated project {} from [{}]".format(mutated_project_name, project_dir))
    return current_mutated_project_dir


def get_feature_name_from_mutated_project_name(mutated_project_dir):
    return get_project_name(mutated_project_dir).split(".", 1)[0]


def check_bug_from_report(mutated_project_dir, must_interaction_bug=True):
    # logger.info(f"Writing test output to project's configs report [{get_file_name(project_dir)}]")
    configs_report_file_path = get_model_configs_report_path(mutated_project_dir)
    feature_name = get_feature_name_from_mutated_project_name(mutated_project_dir)
    exist_failing_configuration = False
    is_interaction_bug = False
    with open(configs_report_file_path, "r") as report_csv:
        reader = csv.reader(report_csv)
        header = next(reader)
        feature_column_index = header.index(feature_name)
        for i, row in enumerate(reader):
            feature_was_enabled = row[feature_column_index].strip() == "T"
            all_test_passed = row[-1] == "__PASSED__"
            if not all_test_passed:
                exist_failing_configuration = True
            if feature_was_enabled and all_test_passed:
                is_interaction_bug = True

    return exist_failing_configuration and (must_interaction_bug and is_interaction_bug)

import csv
from itertools import combinations

from FileManager import get_plugin_path, split_path, get_mutation_result_dir, list_dir, join_path, \
    get_mutated_projects_dir, create_symlink, get_feature_source_code_dir, get_file_name_without_ext, copy_dir, \
    is_path_exist, get_model_configs_report_path, get_project_name, unlink, is_symlink
from Helpers import get_logger, execute_shell_command, hash_md5
from SuspiciousStatementManager import get_buggy_statement

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


def mixing_multiple_bugs(mutant_paths, num_of_bugs=1):
    if num_of_bugs == 0:
        return []
    elif num_of_bugs == 1:
        return [(source_file_path,) for source_file_path in mutant_paths]
    else:
        deduplicated_bug_dict = {}
        for source_file_path in mutant_paths:
            mutant_path_parts = source_file_path.rsplit("/", 5)
            operator_index = mutant_path_parts[4]
            full_class_name = mutant_path_parts[1]
            global_bug_id = full_class_name
            if global_bug_id not in deduplicated_bug_dict:
                deduplicated_bug_dict[global_bug_id] = source_file_path
        mixed_mutant_path_tuples = list(combinations(deduplicated_bug_dict.values(), num_of_bugs))
        return mixed_mutant_path_tuples


def generate_mutants(project_dir, optional_feature_names, num_of_bugs=1):
    logger.info(f"Mutating features [{get_file_name_without_ext(project_dir)}]")
    assign_current_project_as_new_session(project_dir)
    mutant_paths = make_mutants(project_dir, optional_feature_names)
    mutant_path_tuples = mixing_multiple_bugs(mutant_paths, num_of_bugs=num_of_bugs)
    mutated_project_dirs = inject_mutants(project_dir, mutant_path_tuples)
    return mutated_project_dirs


def inject_mutants(project_dir, mutant_path_tuples):
    logger.info(f"Injecting mutants to features [{get_file_name_without_ext(project_dir)}]")
    mutated_projects_dir = get_mutated_projects_dir(project_dir)
    features_dir = get_feature_source_code_dir(project_dir)
    mutated_project_dirs = []
    for tuple_index, mutant_path_tuple in enumerate(mutant_path_tuples):
        # FORMAT: ~/InputPreparation/projects/GPL-Test/mutation_result/DirectedWithEdges.GPL.Edge/traditional_mutants/Vertex_getOtherVertex(Vertex)/ROR_1/Edge.java'
        current_project_name = "_MultipleBugs_.NOB_{}.ID_{}".format(len(mutant_path_tuple), tuple_index + 1)
        current_mutated_project_dir = join_path(mutated_projects_dir, current_project_name)
        current_mutated_features_dir = get_feature_source_code_dir(project_dir=current_mutated_project_dir)
        final_mutation_log = ""
        for mutant_path in mutant_path_tuple:
            mutant_path_parts = mutant_path.rsplit("/", 5)
            full_class_name = mutant_path_parts[1]
            package, class_name = full_class_name.rsplit(".", 1)
            class_name += ".java"
            operator_index = mutant_path_parts[4]
            bug_name = f"{full_class_name}.{operator_index}"
            mutation_log_file = join_path(*mutant_path_parts[:-3], "mutation_logs", f"{bug_name}.log")
            with open(mutation_log_file) as f:
                # append more line hint to final log file
                # line log:  ODL_2:32:void_enterElevator(Person):weight += p.getWeight() => weight = p.getWeight()
                mutated_line_hints = f.readlines()[0].split(":", 2)
                mutated_line_hints[0] = bug_name
                joined_line_hint = ":".join(mutated_line_hints)
                final_mutation_log += joined_line_hint

            for feature_name in list_dir(features_dir):
                current_feature_dir = join_path(features_dir, feature_name)
                current_mutated_feature_dir = join_path(current_mutated_features_dir, feature_name)

                if feature_name == package.split(".")[0]:
                    if is_path_exist(current_mutated_feature_dir):
                        # feature dir already copied, keep this and create symlink from mutated java file to this dir
                        if not is_symlink(current_mutated_feature_dir):
                            continue
                        unlink(current_mutated_feature_dir)
                    copy_dir(current_feature_dir, current_mutated_feature_dir)

                else:
                    if not is_path_exist(current_mutated_feature_dir):
                        create_symlink(current_feature_dir, current_mutated_feature_dir)

            mutant_path_dst = join_path(current_mutated_features_dir, *package.split("."), class_name)
            create_symlink(mutant_path, mutant_path_dst)

        # write mutated line position to final mutated log for tracing
        mutated_project_mutation_log_file = join_path(current_mutated_project_dir,
                                                      f"{current_project_name}.mutant.log")
        with open(mutated_project_mutation_log_file, "w+") as f:
            f.write(final_mutation_log)

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


def check_bug_from_report(mutated_project_dir):
    # logger.info(f"Writing test output to project's configs report [{get_file_name(project_dir)}]")
    configs_report_file_path = get_model_configs_report_path(mutated_project_dir)
    exist_passing_configuration = False
    exist_failing_configuration = False
    with open(configs_report_file_path, "r") as report_csv:
        reader = csv.reader(report_csv)
        next(reader)
        for i, row in enumerate(reader):
            test_passed = row[-1] == "__PASSED__"
            if test_passed:
                exist_passing_configuration = True
            else:
                exist_failing_configuration = True
    is_bug_satisfied = (exist_passing_configuration and exist_failing_configuration)
    return is_bug_satisfied

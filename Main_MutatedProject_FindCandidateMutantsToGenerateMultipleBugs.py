from collections import defaultdict
from itertools import combinations, product

import MutantManager
from FileManager import get_project_dir, get_file_name
from suspicious_statements_manager.SuspiciousStatementManager import get_mutation_operators

if __name__ == "__main__":
    # ------ START CONFIG ------
    base_dir = "/Users/tuanngokien/Desktop/Software_Analysis/configurable_system/dataset"
    project_name = "4wise-Elevator-FH-JML-NOB2"
    # ------ END CONFIG ------

    project_dir = get_project_dir(project_name, base_dir)

    mutated_project_dirs = MutantManager.get_mutated_project_dirs(project_dir, sort=True)
    current_number_of_bugs = -1
    current_mutation_operator_combinations = set()
    mutation_operator_with_file_mapping = defaultdict(set)
    target_number_of_bugs = -1
    for mutated_project_dir in mutated_project_dirs:
        mutated_project_name = get_file_name(mutated_project_dir)
        mutation_operators = get_mutation_operators(mutated_project_name, mutated_project_dir)
        current_mutation_operator_combinations.add(tuple(mutation_operators))
        for o in mutation_operators:
            file_id = o.rsplit(".", 1)[0]
            mutation_operator_with_file_mapping[file_id].add(o)
        if current_number_of_bugs < 0:
            current_number_of_bugs = len(mutation_operators)

    target_number_of_bugs = current_number_of_bugs + 1
    # read MutantManager.mixing_multiple_bugs function for the loop below
    target_number_of_bugs_combinations = []
    for c in combinations(mutation_operator_with_file_mapping.values(), target_number_of_bugs):
        target_number_of_bugs_combinations.extend(list(product(*c)))

    # recheck that fixing a random bug always results in a valid existing combinations (3 bugs -> 2 bugs)
    for bug_combination in target_number_of_bugs_combinations[:]:
        for c in combinations(bug_combination, current_number_of_bugs):
            if c not in current_mutation_operator_combinations:
                target_number_of_bugs_combinations.remove(bug_combination)
                break
    print(len(target_number_of_bugs_combinations))

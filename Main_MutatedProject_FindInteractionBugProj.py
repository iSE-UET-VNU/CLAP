import MutantManager

from FileManager import get_project_dir, get_project_name, get_file_name
from SuspiciousStatementManager import get_buggy_statement

if __name__ == "__main__":
    project_name = "3wise-Mutated-GPL-Test"
    project_dir = get_project_dir(project_name)

    mutated_project_dirs = MutantManager.get_mutated_project_dirs(project_dir)
    for mutated_project_dir in mutated_project_dirs:
        mutated_project_name = get_project_name(mutated_project_dir)
        is_interaction_bug = MutantManager.check_bug_from_report(mutated_project_dir, must_interaction_bug=False)
        if is_interaction_bug:
            print(
                f"[{get_buggy_statement(mutated_project_name, mutated_project_dir)}] - {get_file_name(mutated_project_dir)}")

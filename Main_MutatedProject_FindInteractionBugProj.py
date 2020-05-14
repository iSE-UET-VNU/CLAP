import MutantManager

from FileManager import get_project_dir

if __name__ == "__main__":
    project_name = "3wise-Mutated-GPL-Test"
    project_dir = get_project_dir(project_name)

    mutated_project_dirs = MutantManager.get_mutated_project_dirs(project_dir)
    for mutated_project_dir in mutated_project_dirs:
        is_interaction_bug = MutantManager.check_interaction_bug_from_report(mutated_project_dir)
        if is_interaction_bug:
            print(mutated_project_dir)

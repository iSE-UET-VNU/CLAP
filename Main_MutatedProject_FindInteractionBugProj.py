import MutantManager

from FileManager import get_project_dir, get_file_name

if __name__ == "__main__":
    project_name = "2wise-BankAccountTP"
    project_dir = get_project_dir(project_name)

    mutated_project_dirs = MutantManager.get_mutated_project_dirs(project_dir)
    for mutated_project_dir in mutated_project_dirs:
        buggy_statement, has_bug = MutantManager.check_bug_from_report(mutated_project_dir, must_interaction_bug=False)
        if has_bug:
            print(f"[{buggy_statement}] - {get_file_name(mutated_project_dir)}")

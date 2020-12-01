import MutantManager

from FileManager import get_project_dir

if __name__ == "__main__":
    base_dir = "/Users/tuanngokien/Desktop/Software_Analysis/configurable_system/dataset"
    project_name = "2wise-Email-FH-JML-MB-Full"
    project_dir = get_project_dir(project_name, base_dir)

    mutated_project_dirs = MutantManager.get_mutated_project_dirs(project_dir, sort=True)
    for mutated_project_dir in mutated_project_dirs:
        has_bug = MutantManager.check_bug_from_report(mutated_project_dir)
        if has_bug:
            print(f"{mutated_project_dir}")

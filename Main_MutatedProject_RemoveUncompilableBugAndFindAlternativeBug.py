import MutantManager
from AntManager import check_all_variant_compilable

from FileManager import get_project_dir, get_dependency_lib_dirs, get_file_name

if __name__ == "__main__":
    # ------ START CONFIG ------
    base_dir = "/Users/tuanngokien/Desktop/Software_Analysis/configurable_system/dataset"
    project_name = "2wise-Email-FH-JML-MB-Full"
    preferred_bugs = []
    # ------ END CONFIG ------

    project_dir = get_project_dir(project_name, base_dir)
    lib_paths = get_dependency_lib_dirs(project_dir)

    mutated_projects_dir = MutantManager.get_mutated_projects_dir(project_dir)
    selected_mutated_project_dirs = MutantManager.get_mutated_project_dirs(project_dir, sort=True)
    selected_bugs = set()
    uncompilable_bugs = set()
    for mutated_project_dir in selected_mutated_project_dirs:
        bug_name = get_file_name(mutated_project_dir)
        selected_bugs.add(bug_name)
        if len(preferred_bugs) > 0 and bug_name not in preferred_bugs:
            continue
        is_compilable = check_all_variant_compilable(mutated_project_dir, lib_paths=lib_paths)
        if not is_compilable:
            uncompilable_bugs.add(bug_name)
    print("-------- #UNCOMPILABLE BUGS --------")
    for bug_name in uncompilable_bugs:
        print(bug_name)
    print("-------- #ALTERNATIVE BUGS --------")
    reselected_bugs = set()
    all_get_mutated_project_dirs = MutantManager.get_mutated_project_dirs(project_dir, include_temp_project_dir=True,
                                                                          sort=True)
    for mutated_project_dir in all_get_mutated_project_dirs:
        bug_name = get_file_name(mutated_project_dir)
        if bug_name in uncompilable_bugs:
            continue
        has_bug = MutantManager.check_bug_from_report(mutated_project_dir, recheck_compilable=True, lib_paths=lib_paths)
        if has_bug:
            reselected_bugs.add(bug_name)

    for bug_name in (reselected_bugs - selected_bugs):
        print(bug_name)

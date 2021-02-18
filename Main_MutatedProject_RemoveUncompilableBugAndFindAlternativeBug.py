import MutantManager
from AntManager import check_source_code_compilable

from FileManager import get_project_dir, get_all_variant_dirs, get_dependency_lib_dirs, get_file_name_without_ext

if __name__ == "__main__":
    # ------ START CONFIG ------
    base_dir = "/Users/tuanngokien/Desktop/Software_Analysis/configurable_system/dataset"
    project_name = "2wise-Email-FH-JML-MB-Full"
    # ------ END CONFIG ------

    project_dir = get_project_dir(project_name, base_dir)
    lib_paths = get_dependency_lib_dirs(project_dir)

    mutated_project_dirs = MutantManager.get_mutated_project_dirs(project_dir, sort=True)
    print("-------- #UNCOMPILABLE BUGS --------")
    for mutated_project_dir in mutated_project_dirs:
        variant_dirs = get_all_variant_dirs(mutated_project_dir, sort=True)
        for variant_dir in variant_dirs:
            is_compilable = check_source_code_compilable(variant_dir, lib_paths=lib_paths)
            if not is_compilable:
                print(f"{get_file_name_without_ext(mutated_project_dir)} - {variant_dir}")
                break
    # print("-------- #UNCOMPILABLE BUGS --------")

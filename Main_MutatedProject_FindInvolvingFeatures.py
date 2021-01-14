import InvolvingFeatureManager
import MutantManager
import TestManager

from FileManager import list_dir, get_project_dir, lock_project

if __name__ == "__main__":
    # ------ START CONFIG ------
    base_dir = "/Users/tuanngokien/Desktop/Software_Analysis/configurable_system/dataset"
    project_name = "1wise-GPL"
    # ------ END CONFIG ------

    project_dir = get_project_dir(project_name, base_dir)
    mutated_project_dirs = MutantManager.get_mutated_project_dirs(project_dir, sort=True)
    for mutated_project_dir in mutated_project_dirs:
        try:
            lock_project(mutated_project_dir)
        except BlockingIOError as e:
            continue
        InvolvingFeatureManager.find_involving_feature(project_dir, mutated_project_dir)

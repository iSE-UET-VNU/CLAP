import AntManager
import InvolvingFeatureManager
import MutantManager

from FileManager import get_project_dir, lock_project

if __name__ == "__main__":
    # ------ START CONFIG ------
    base_dir = "/Users/tuanngokien/Desktop/Software_Analysis/configurable_system/dataset"
    project_name = "4wise-BankAccountTP-FH-JML"
    # ------ END CONFIG ------

    project_dir = get_project_dir(project_name, base_dir)
    mutated_project_dirs = MutantManager.get_mutated_project_dirs(project_dir, sort=True)
    cloned_ant_name = AntManager.clone_ant_plugin()
    for mutated_project_dir in mutated_project_dirs:
        try:
            lock_project(mutated_project_dir)
        except BlockingIOError as e:
            continue
        try:
            InvolvingFeatureManager.find_involving_feature(project_dir, mutated_project_dir, custom_ant=cloned_ant_name)
        except Exception:
            continue

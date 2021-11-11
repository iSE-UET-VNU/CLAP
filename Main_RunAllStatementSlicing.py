from FileManager import list_dir, lock_project
from suspicious_statements_manager import SlicingManager

if __name__ == "__main__":
    # ------ START CONFIG ------
    mutants_dir = "/Users/tuanngokien/Desktop/Software_Analysis/configurable_system/dataset/4wise-ZipMe"
    # ------ END CONFIG ------π

    mutated_project_dirs = list_dir(mutants_dir, full_path=True)

    # clone ant directory
    # cloned_ant_name = AntManager.clone_ant_plugin()

    # run junit test with coverage and write to project's configs report
    for mutated_project_dir in mutated_project_dirs:
        try:
            lock_project(mutated_project_dir)
        except BlockingIOError as e:
            pass

        SlicingManager.do_slice_all_statements(mutated_project_dir)
        break

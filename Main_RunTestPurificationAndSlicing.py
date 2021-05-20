import AntManager
import TestManager

from FileManager import list_dir, lock_project
from slice_based_manager import TestPurificationManager
from suspicious_statements_manager import SlicingManager

if __name__ == "__main__":
    # ------ START CONFIG ------
    mutants_dir = "/home/hieuvd/spl_dataset_generation/InputPreparation/new_projects/4wise-ZipMe/mutated_projects"
    # ------ END CONFIG ------π

    mutated_project_dirs = list_dir(mutants_dir, full_path=True)

    # clone ant directory
    cloned_ant_name = AntManager.clone_ant_plugin()

    # run junit test with coverage and write to project's configs report
    for mutated_project_dir in mutated_project_dirs:
        try:
            lock_project(mutated_project_dir)
        except BlockingIOError as e:
            continue

        failed_variant_dirs = TestManager.get_failed_variant_dirs_from_config_report(mutated_project_dir)
        # TestManager.run_batch_junit_test_cases_on_project(mutated_project_dir,
        #                                                   custom_ant=cloned_ant_name,
        #                                                   custom_variant_dirs=failed_variant_dirs)
        pts_file_path = TestPurificationManager.generate_purified_test_suite(mutated_project_dir, failed_variant_dirs)
        SlicingManager.do_slice_pts(pts_file_path)

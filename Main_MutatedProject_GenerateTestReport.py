import AntManager
import MutantManager
import TestManager

from FileManager import get_project_dir, lock_project
from Helpers import sleep
from VariantComposer import was_variants_composed

if __name__ == "__main__":
    project_name = "GPL-Test"
    project_dir = get_project_dir(project_name)

    # clone ant directory
    cloned_ant_name = AntManager.clone_ant_plugin()

    # run junit test with coverage and write to project's configs report
    while True:
        mutated_project_dirs = MutantManager.get_mutated_project_dirs(project_dir)
        for mutated_project_dir in mutated_project_dirs:
            if not was_variants_composed(mutated_project_dir):
                continue
            try:
                lock_project(mutated_project_dir)
            except BlockingIOError as e:
                continue
            TestManager.run_junit_test_cases_with_coverage_on_project(mutated_project_dir, cloned_ant_name)
            TestManager.write_test_output_to_configs_report(mutated_project_dir)
        sleep(1800)

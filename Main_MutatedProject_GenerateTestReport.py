import AntManager
import MutantManager
import TestManager

from FileManager import get_project_dir, lock_project
from Helpers import sleep, natural_sort
from VariantComposer import was_variants_composed

if __name__ == "__main__":
    base_dir = None
    project_name = "3wise-Mutated-Elevator-FH-JML"
    project_dir = get_project_dir(project_name, base_dir)

    # clone ant directory
    cloned_ant_name = AntManager.clone_ant_plugin()

    # run junit test with coverage and write to project's configs report
    while True:
        mutated_project_dirs = MutantManager.get_mutated_project_dirs(project_dir)
        mutated_project_dirs = natural_sort(mutated_project_dirs)
        for mutated_project_dir in mutated_project_dirs:
            if not was_variants_composed(mutated_project_dir):
                continue
            try:
                lock_project(mutated_project_dir)
            except BlockingIOError as e:
                continue
            try:
                TestManager.run_junit_test_cases_with_coverage_on_project(mutated_project_dir, cloned_ant_name)
            except RuntimeError:
                continue
            else:
                TestManager.write_test_output_to_configs_report(mutated_project_dir)
        sleep(1800)

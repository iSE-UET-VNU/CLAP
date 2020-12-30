import MutantManager
import SpectrumCoverageManager
from FileManager import get_project_dir, lock_project
from Helpers import sleep

if __name__ == "__main__":
    # ------ START CONFIG ------
    base_dir = "/Users/tuanngokien/Desktop/Software_Analysis/configurable_system/dataset"
    project_name = "4wise-Email-FH-JML"
    # ------ END CONFIG ------

    project_dir = get_project_dir(project_name, base_dir)
    while True:
        mutated_project_dirs = MutantManager.get_mutated_project_dirs(project_dir, sort=True)
        for mutated_project_dir in mutated_project_dirs:
            try:
                lock_project(mutated_project_dir)
            except BlockingIOError as e:
                continue
            SpectrumCoverageManager.rebuild_incremental_spectrum_coverages(mutated_project_dir)
        sleep(1800)

import MutantManager
import TestCoverageValidator

from FileManager import get_project_dir

if __name__ == "__main__":
    # ------ START CONFIG ------
    base_dir = "/Users/tuanngokien/Desktop/Software_Analysis/configurable_system/dataset"
    project_name = "1wise-Email-FH-JML"
    # ------ END CONFIG ------

    project_dir = get_project_dir(project_name, base_dir)

    mutated_project_dirs = MutantManager.get_mutated_project_dirs(project_dir, sort=True)

    for mutated_project_dir in mutated_project_dirs:
        TestCoverageValidator.check(mutated_project_dir)
        break

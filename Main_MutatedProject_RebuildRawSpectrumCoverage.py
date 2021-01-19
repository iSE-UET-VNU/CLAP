import SpectrumCoverageManager
from FileManager import list_dir
from Helpers import get_logger

logger = get_logger(__name__)

if __name__ == "__main__":
    # ------ START CONFIG ------
    base_dir = "/Users/tuanngokien/Desktop/Software_Analysis/configurable_system/dataset/4wise-BankAccountTP-FH-JML/mutated_projects"
    version = ""
    # ------ END CONFIG ------

    mutated_project_dirs = list_dir(base_dir, full_path=True, sort=True)
    for mutated_project_dir in mutated_project_dirs:
        try:
            SpectrumCoverageManager.rebuild_spectrum_coverage_for_mutated_project(
                mutated_project_dir=mutated_project_dir, version=version)
        except Exception as e:
            logger.exception(e)
            continue

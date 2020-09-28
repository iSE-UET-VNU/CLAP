import CoverageManager
import MutantManager
from FileManager import get_project_dir
from Helpers import get_version_by_time

if __name__ == "__main__":
    # version = "20200928_011024"
    version = get_version_by_time()
    base_dir = "/Users/tuanngokien/Desktop/Software_Analysis/configurable_system/InputPreparation/projects/"
    project_name = "Elevator-FH-JML"
    project_dir = get_project_dir(project_name, base_dir)
    mutated_project_name = "Empty.ElevatorSystem.Environment.ROR_1"
    mutated_project_dir = MutantManager.get_mutated_project_dir(project_dir, mutated_project_name)
    spc_log_file_path = CoverageManager.rebuild_spectrum_coverage_for_mutated_project(mutated_project_dir,
                                                                                      version=version)

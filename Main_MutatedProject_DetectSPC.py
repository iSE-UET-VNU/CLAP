import MutantManager
import SPCsManager
import SlicingManager

from FileManager import get_project_dir

if __name__ == "__main__":
    project_name = "Elevator-FH-JML"
    project_dir = get_project_dir(project_name)
    mutated_project_name = "Empty.ElevatorSystem.Environment.AOIS_1"

    mutated_project_dir = MutantManager.get_mutated_project_dir(project_dir, mutated_project_name)

    spc_log_file_path = SPCsManager.find_SPCs(mutated_project_dir, 0.5)
    SlicingManager.do_slice(spc_log_file_path, 0.5)
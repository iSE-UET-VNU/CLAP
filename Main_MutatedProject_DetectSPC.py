import MutantManager
import SPCsManager

from FileManager import get_project_dir

if __name__ == "__main__":
    project_name = "Mutated-GPL-Test"
    project_dir = get_project_dir(project_name)
    mutated_project_name = "BFS.GPL.Graph.COD_1"

    mutated_project_dir = MutantManager.get_mutated_project_dir(project_dir, mutated_project_name)

    SPCsManager.find_SPCs(mutated_project_dir)

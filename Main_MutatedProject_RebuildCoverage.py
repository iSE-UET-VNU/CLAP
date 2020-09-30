import CoverageManager
import MutantManager
from FileManager import get_project_dir, get_mutated_projects_dir, list_dir
from Helpers import get_version_by_time

if __name__ == "__main__":
    # version = "20200928_011024"
    version = "v2"
    base_dir = "/Users/thu-trangnguyen/Documents/Research/configurable_system/Experiment/projects/Email/"
    project_names = ["4wise"]
    for project in project_names:
        project_dir = get_project_dir(project, base_dir)
        mutated_projects_dir = get_mutated_projects_dir(project_dir)
        mutated_projects = list_dir(mutated_projects_dir)
        for mutated_project_name in mutated_projects:
            #mutated_project_name = "AutoResponder.EmailSystem.Client.COI_2"
            mutated_project_dir = MutantManager.get_mutated_project_dir(project_dir, mutated_project_name)
            spc_log_file_path = CoverageManager.rebuild_spectrum_coverage_for_mutated_project(mutated_project_dir,
                                                                                          version=version)

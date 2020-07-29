import MutantManager
from FileManager import get_project_dir, get_mutated_projects_dir, list_dir
from TestingCoverageManager import statement_coverage_of_variants

if __name__ == "__main__":
    base_dir = "/Users/thu-trangnguyen/Documents/Research/configurable_system/Experiment/projects"
    project_name = "4wise-Mutated-GPL-Test3"
    project_dir = get_project_dir(project_name, base_dir)
    mutated_projects_dir = get_mutated_projects_dir(project_dir)
    mutated_projects = list_dir(mutated_projects_dir)

    for mutated_project_name in mutated_projects:
        mutated_project_dir = MutantManager.get_mutated_project_dir(project_dir, mutated_project_name)
        print(mutated_project_name)
        print(statement_coverage_of_variants(mutated_project_dir))
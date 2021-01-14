import InvolvingFeatureManager
import MutantManager

from FileManager import list_dir, get_project_dir

if __name__ == "__main__":
    base_dir = "/Users/tuanngokien/Desktop/Software_Analysis/configurable_system/dataset"
    project_name = "1wise-GPL"
    project_dir = get_project_dir(project_name, base_dir)

    mutated_project_dirs = MutantManager.get_mutated_project_dirs(project_dir, sort=True)
    for mutated_project_dir in mutated_project_dirs:
        print(mutated_project_dir)
        InvolvingFeatureManager.find_involving_feature(project_dir, mutated_project_dir)
        break
        # has_bug = MutantManager.check_bug_from_report(mutated_project_dir)
        # if has_bug:
        #     print(f"{mutated_project_dir}")

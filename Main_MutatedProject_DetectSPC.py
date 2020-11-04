import MutantManager
import SPCsManager
import SlicingManager

from FileManager import get_project_dir

if __name__ == "__main__":
    coverage_version = ""
    project_name = "4wise-BankAccountTP"
    base_dir = "/Users/tuanngokien/Desktop/Software_Analysis/configurable_system/dataset/"
    project_dir = get_project_dir(project_name, base_dir)
    mutated_project_name = "DailyLimit.Account.AOIS_7"

    mutated_project_dir = MutantManager.get_mutated_project_dir(project_dir, mutated_project_name)
    spc_log_file_path = SPCsManager.find_SPCs(mutated_project_dir, 0.95)
    SlicingManager.do_slice(spc_file_path=spc_log_file_path, filtering_coverage_rate=0.95,
                            coverage_version=coverage_version)

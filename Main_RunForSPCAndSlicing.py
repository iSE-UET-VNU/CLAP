import MutantManager
from FileManager import list_dir, get_spc_log_file_path, join_path
from spc import SPCsManager
from suspicious_statements_manager import SlicingManager

if __name__ == "__main__":
    mutants_dir = ""
    mutants = list_dir(mutants_dir)
    coverage = 0.0
    for mutant_name in mutants:
        mutated_project_dir = join_path(mutants_dir, mutant_name)
        SPCsManager.find_SPCs(mutated_project_dir, coverage=0.0)
        spc_log_file_path = get_spc_log_file_path(mutated_project_dir, coverage)
        slicing_runtime = SlicingManager.do_slice(spc_log_file_path, coverage, "")
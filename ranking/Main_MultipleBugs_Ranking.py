from FileManager import join_path
from MultipleBugsManager import mutiple_bugs_ranking
from Spectrum_Expression import TARANTULA, OP2, OCHIAI, BARINEL, DSTAR

if __name__ == "__main__":
    result_folder = "multiple_bugs_"
    base_dir = "/home/huent/Documents/Trang/Mixed_Multiple_bugs/"
    system_names = ["Elevator2new", "Elevator3new"]
    filtering_coverage_rate_list = [0.1]
    for system_name in system_names:
        system_dir = join_path(base_dir, system_name)
        for coverage in filtering_coverage_rate_list:
            print(system_dir)
            mutiple_bugs_ranking(result_folder, system_name, system_dir, [OCHIAI, OP2, TARANTULA], coverage)
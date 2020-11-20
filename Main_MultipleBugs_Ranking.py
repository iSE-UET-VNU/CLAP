from FileManager import join_path
from MultipleBugsManager import mutiple_bugs_ranking
from Spectrum_Expression import TARANTULA, OP2, OCHIAI, BARINEL, DSTAR

if __name__ == "__main__":
    base_dir = "/home/huent/Documents/Trang/Multiple_bugs/"
    system_name = "Elevator"
    system_dir = join_path(base_dir, system_name)
    filtering_coverage_rate_list = [0.0]
    for coverage in filtering_coverage_rate_list:
        print(system_dir)
        mutiple_bugs_ranking(system_name, system_dir, [TARANTULA, OCHIAI, OP2, BARINEL, DSTAR], coverage)
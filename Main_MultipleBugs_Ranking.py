from FileManager import join_path
from MultipleBugsManager import mutiple_bugs_ranking
from Spectrum_Expression import TARANTULA, OP2

if __name__ == "__main__":
    base_dir = "/Users/thu-trangnguyen/Documents/Research/configurable_system/Experiment/projects/multiple_bugs"
    system_name = "_MultipleBugs_.NOB_2.ID_2"
    system_dir = join_path(base_dir, system_name)
    filtering_coverage_rate_list = [0.95]
    for coverage in filtering_coverage_rate_list:
        #print(system_dir)
        mutiple_bugs_ranking(system_name, system_dir, [TARANTULA, OP2], coverage)
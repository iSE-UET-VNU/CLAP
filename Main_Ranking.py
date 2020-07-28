import threading

from ExperimentResultManager import ranking_with_coverage_rate
from RankingManager import TARANTULA, OCHIAI, OP2, BARINEL, DSTAR, WORST_CASE, BEST_CASE

if __name__ == "__main__":

    base_dir = "/Users/thu-trangnguyen/Documents/Research/configurable_system/Experiment/projects/Email"
    system_name = "Email"
    project_names = ["4wise"]

    filtering_coverage_rate_list = [0.95]
    for coverage_index in range(0, len(filtering_coverage_rate_list)):
         for project_index in range(0, len(project_names)):
            #ranking_with_coverage_rate(base_dir, project_names[project_index], filtering_coverage_rate_list[coverage_index], [TARANTULA, OCHIAI, OP2, BARINEL, DSTAR])
            ranking_with_coverage_rate(base_dir, system_name, project_names[project_index],
                                       filtering_coverage_rate_list[coverage_index],
                                       [DSTAR], WORST_CASE)



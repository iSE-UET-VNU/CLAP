import threading

from ExperimentResultManager import ranking_with_coverage_rate
from RankingManager import TARANTULA, OCHIAI, OP2, BARINEL, DSTAR

if __name__ == "__main__":

    base_dir = "/Users/thu-trangnguyen/Documents/Research/configurable_system/Experiment/projects"
    project_names = ["3wise-Mutated-Elevator-FH-JML"]

    filtering_coverage_rate_list = [0.5]
    for coverage_index in range(0, len(filtering_coverage_rate_list)):
         for project_index in range(0, len(project_names)):
            ranking_with_coverage_rate(base_dir, project_names[project_index], filtering_coverage_rate_list[coverage_index], [TARANTULA, OCHIAI, OP2, BARINEL, DSTAR])




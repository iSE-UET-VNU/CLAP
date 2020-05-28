import threading

from ExperimentResultManager import ranking_with_coverage_rate
from RankingManager import TARANTULA, OCHIAI

if __name__ == "__main__":

    base_dir = "/Users/thu-trangnguyen/Documents/Research/configurable_system/Experiment/projects"
    project_names = ["2wise-Mutated-Elevator-FH-JML"]


    filtering_coverage_rate_list = [0.5]

    for coverage_index in range(0, len(filtering_coverage_rate_list)):
         threads = []
         for project_index in range(0, len(project_names)):
            threads.append(threading.Thread(target = ranking_with_coverage_rate, args = (base_dir, project_names[project_index], filtering_coverage_rate_list[coverage_index], [TARANTULA, OCHIAI])))
            threads[project_index].start()

         for project_index in range(0, len(project_names)):
             threads[project_index].join()




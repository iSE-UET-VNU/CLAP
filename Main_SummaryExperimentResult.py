from ExperimentResultManager import summary_experiment_result
from FileManager import get_experimental_result_file

if __name__ == "__main__":
    result_file_name = "4wise-Mutated-GPL-Test_0.5_result.xlsx"
    result_file_path = get_experimental_result_file(result_file_name)
    summary_experiment_result(result_file_path)
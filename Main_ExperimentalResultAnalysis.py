from ExperimentalResultsAnalyzer import summary_result, summary_for_same_bugs, \
    calculate_average_in_a_file_and_write_to_console, count_total_bugs

if __name__ == "__main__":
    #evaluation_type = "best_case"
    #system_names = ["BankAccountTP", "Elevator", "Email", "ExamDB"]
    #num_of_program_stms = {"BankAccountTP":143, "Elevator":854, "Email": 439, "ExamDB": 513}
    #summary_result(evaluation_type, system_names, num_of_program_stms)

    files_list = {"1wise":"/Users/thu-trangnguyen/Documents/project/InputPreparation/experiment_results/best_case/Email/1wise/0.8_best_case.xlsx", "2wise":"/Users/thu-trangnguyen/Documents/project/InputPreparation/experiment_results/best_case/Email/2wise/0.8_best_case.xlsx", "3wise":"/Users/thu-trangnguyen/Documents/project/InputPreparation/experiment_results/best_case/Email/3wise/0.8_best_case.xlsx", "4wise":"/Users/thu-trangnguyen/Documents/project/InputPreparation/experiment_results/best_case/Email/4wise/0.8_best_case.xlsx"}
    #summary_for_same_bugs(files_list, 513)
    print(count_total_bugs(files_list))
    #calculate_average_in_a_file_and_write_to_console("/Users/thu-trangnguyen/Documents/project/InputPreparation/experiment_results/Email/4wise/0.95.xlsx", 439)
from ExperimentalResultsAnalyzer import summary_result, summary_for_same_bugs,  count_total_bugs

if __name__ == "__main__":
    evaluation_type = "worst_case"
    system_names = ["BankAccountTP", "Elevator", "Email", "ExamDB", "GPL"]
    num_of_program_stms = {"BankAccountTP":143, "Elevator":854, "Email": 439, "ExamDB": 513, "GPL": 1944}
    summary_result(evaluation_type, system_names, num_of_program_stms)

    files_list = {"1wise":"/Users/thu-trangnguyen/Documents/project/InputPreparation/experiment_results/worst_case/GPL/1wise/0.8_worst_case.xlsx", "2wise":"/Users/thu-trangnguyen/Documents/project/InputPreparation/experiment_results/worst_case/GPL/2wise/0.8_worst_case.xlsx", "3wise":"/Users/thu-trangnguyen/Documents/project/InputPreparation/experiment_results/worst_case/GPL/3wise/0.8_worst_case.xlsx", "4wise":"/Users/thu-trangnguyen/Documents/project/InputPreparation/experiment_results/worst_case/GPL/4wise/0.8_worst_case.xlsx"}
    #summary_for_same_bugs(files_list, 1944)
    #print(count_total_bugs(files_list))
    #calculate()487_average_in_a_file_and_write_to_console("/Users/thu-trangnguyen/Documents/project/InputPreparation/experiment_results/Email/4wise/0.95.xlsx", 439)
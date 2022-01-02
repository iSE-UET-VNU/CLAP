from collections import defaultdict

from PassingVariants_Classification import *

if __name__ == "__main__":
    system_paths = defaultdict(dict)
    system_paths["BankAccountTP"]["1Bug"] = "/Users/thu-trangnguyen/Documents/Research/SPL/BankAccountTP/1Bug/4wise/"
    system_paths["BankAccountTP"]["2Bug"] = "/Users/thu-trangnguyen/Documents/Research/SPL/BankAccountTP/2Bug/4wise/"
    system_paths["BankAccountTP"]["3Bug"] = "/Users/thu-trangnguyen/Documents/Research/SPL/BankAccountTP/3Bug/4wise/"
    system_paths["Elevator"]["1Bug"] = "/Users/thu-trangnguyen/Documents/Research/SPL/Elevator/1Bug/4wise/"
    system_paths["Elevator"]["2Bug"] = "/Users/thu-trangnguyen/Documents/Research/SPL/Elevator/2Bug/4wise/"
    system_paths["Elevator"]["3Bug"] = "/Users/thu-trangnguyen/Documents/Research/SPL/Elevator/3Bug/4wise/"
    system_paths["Email"]["1Bug"] = "/Users/thu-trangnguyen/Documents/Research/SPL/Email/1Bug/4wise/"
    system_paths["Email"]["2Bug"] = "/Users/thu-trangnguyen/Documents/Research/SPL/Email/2Bug/4wise/"
    system_paths["Email"]["3Bug"] = "/Users/thu-trangnguyen/Documents/Research/SPL/Email/3Bug/4wise/"
    system_paths["ExamDB"]["1Bug"] = "/Users/thu-trangnguyen/Documents/Research/SPL/ExamDB/1Bug/4wise/"
    system_paths["ExamDB"]["2Bug"] = "/Users/thu-trangnguyen/Documents/Research/SPL/ExamDB/2Bug/4wise/"
    system_paths["ExamDB"]["3Bug"] = "/Users/thu-trangnguyen/Documents/Research/SPL/ExamDB/3Bug/4wise/"
    system_paths["GPL"]["1Bug"] = "/Users/thu-trangnguyen/Documents/Research/SPL/GPL/1Bug/1wise/"
    system_paths["ZipMe"]["1Bug"] = "/Users/thu-trangnguyen/Documents/Research/SPL/ZipMe/1Bug/2wise/"

    #label_data(system_paths)
    #calculate_consistent_testing_values_for_features(system_paths, FIELDS)
    do_label_statistics(system_paths)
    #do_features_statistics(system_paths, FIELDS)
    draw_plot(system_paths, "DUU", [DDU])
    # classify_all_cases(system_paths)
    # classify_single_bug_cases(system_paths)
    # classify_by_variants(system_paths)
    # classify_by_systems(system_paths)
    # classify_by_only_a_system(system_paths)

from collections import defaultdict

from PassingVariants_Classification import *
from consistent_testing_manager.LabelData import label_data

if __name__ == "__main__":
    system_paths = defaultdict(dict)
    system_paths["BankAccountTP"]["1Bug"] = "/home/huent/Documents/SPL/BankAccountTP-1Bug/"
    system_paths["BankAccountTP"]["2Bug"] = "/home/huent/Documents/SPL/BankAccountTP-2Bug"
    system_paths["BankAccountTP"]["3Bug"] = "/home/huent/Documents/SPL/BankAccountTP-3Bug"
    system_paths["Elevator"]["1Bug"] = "/home/huent/Documents/SPL/Elevator-1Bug"
    system_paths["Elevator"]["2Bug"] = "/home/huent/Documents/SPL/Elevator-2Bug"
    system_paths["Elevator"]["3Bug"] = "/home/huent/Documents/SPL/Elevator-3Bug"
    system_paths["Email"]["1Bug"] = "/home/huent/Documents/SPL/Email-1Bug"
    system_paths["Email"]["2Bug"] = "/home/huent/Documents/SPL/Email-2Bug"
    system_paths["Email"]["3Bug"] = "/home/huent/Documents/SPL/Email-3Bug"
    system_paths["ExamDB"]["1Bug"] = "/home/huent/Documents/SPL/ExamDB-1Bug"
    system_paths["ExamDB"]["2Bug"] = "/home/huent/Documents/SPL/ExamDB-2Bug"
    system_paths["ExamDB"]["3Bug"] = "/home/huent/Documents/SPL/ExamDB-3Bug"
    system_paths["GPL"]["1Bug"] = "/home/huent/Documents/SPL/GPL-1Bug"
    system_paths["GPL"]["2Bug"] = "/home/huent/Documents/SPL/GPL-2Bug"
    system_paths["GPL"]["3Bug"] = "/home/huent/Documents/SPL/GPL-3Bug"
    system_paths["ZipMe"]["1Bug"] = "/home/huent/Documents/SPL/ZipMe-1Bug"
    system_paths["ZipMe"]["2Bug"] = "/home/huent/Documents/SPL/ZipMe-2Bug"
    system_paths["ZipMe"]["3Bug"] = "/home/huent/Documents/SPL/ZipMe-3Bug"

    version_based_classification(system_paths)
    system_based_classification(system_paths)
    product_based_classification(system_paths)
    within_system_classification(system_paths)
    intrinsic_analysis(system_paths, system_name="BankAccountTP")

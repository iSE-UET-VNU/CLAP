from PassingVariants_Classification import FIELDS
from consistent_testing_manager.FPMatricsCaculation import calculate_consistent_testing_values_for_features

if __name__ == "__main__":
    system_path = "/Users/thu-trangnguyen/Documents/Research/SPL/BankAccountTP/1Bug/4wise/"
    calculate_consistent_testing_values_for_features(system_path, FIELDS)
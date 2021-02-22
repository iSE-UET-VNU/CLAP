import MutantManager
import ConfigManager
import TestManager
import VariantComposer

from FileManager import get_project_dir, get_all_variant_dirs

if __name__ == "__main__":
    # ------ START CONFIG ------
    base_dir = "/home/hieuvd/spl_dataset_generation/InputPreparation/new_projects"
    project_name = "4wise-BankAccountTP-NOB3"
    num_of_seeding_bugs = 1
    case_limit = 10000
    bug_ids = None
    bug_tuples = [('BankAccount.Account.AOIU_8', 'CreditWorthiness.Account.AOIU_1', 'DailyLimit.Account.AOIU_9'),('BankAccount.Account.AOIU_8', 'CreditWorthiness.Account.AOIU_1', 'DailyLimit.Account.AOIU_10'),('BankAccount.Account.AOIU_8', 'CreditWorthiness.Account.AOIU_1', 'DailyLimit.Account.AOIS_42'),('BankAccount.Account.AOIU_8', 'CreditWorthiness.Account.AOIU_1', 'DailyLimit.Account.AOIU_8'),('BankAccount.Account.AOIU_8', 'CreditWorthiness.Account.AOIU_1', 'DailyLimit.Account.COD_2'),('BankAccount.Account.AOIU_8', 'CreditWorthiness.Account.AOIU_1', 'DailyLimit.Account.AOIU_1'),('BankAccount.Account.AOIU_3', 'DailyLimit.Account.COD_2', 'Interest.Account.LOI_1'),('BankAccount.Account.AOIU_3', 'DailyLimit.Account.AOIU_2', 'Interest.Account.LOI_1'),('BankAccount.Account.AOIU_3', 'DailyLimit.Account.AOIU_1', 'Interest.Account.LOI_1'),('BankAccount.Account.AOIU_3', 'DailyLimit.Account.AOIU_4', 'Interest.Account.LOI_1'),('BankAccount.Account.AOIU_3', 'DailyLimit.Account.COD_1', 'Interest.Account.LOI_1'),('BankAccount.Account.AOIU_3', 'DailyLimit.Account.AOIU_7', 'Interest.Account.LOI_1'),('BankAccount.Account.AOIU_7', 'DailyLimit.Account.AOIU_9', 'Interest.Account.LOI_1'),('BankAccount.Account.AOIU_7', 'DailyLimit.Account.AOIU_10', 'Interest.Account.LOI_1'),('DailyLimit.Account.AOIU_8', 'Interest.Account.LOI_1', 'Transaction.Transaction.COD_2'),('DailyLimit.Account.COD_2', 'Interest.Account.LOI_1', 'Transaction.Transaction.AOIU_1'),('DailyLimit.Account.AOIU_2', 'Interest.Account.LOI_1', 'Transaction.Transaction.AOIU_1'),('DailyLimit.Account.AOIU_2', 'Interest.Account.LOI_1', 'Transaction.Transaction.COD_1'),('DailyLimit.Account.AOIU_2', 'Interest.Account.LOI_1', 'Transaction.Transaction.COD_3'),('DailyLimit.Account.AOIU_1', 'Interest.Account.LOI_1', 'Transaction.Transaction.AOIU_1'),('DailyLimit.Account.AOIU_1', 'Interest.Account.LOI_1', 'Transaction.Transaction.COD_1'),('DailyLimit.Account.AOIU_1', 'Interest.Account.LOI_1', 'Transaction.Transaction.COD_3'),('DailyLimit.Account.AOIU_4', 'InterestEstimation.Account.AOIS_1', 'Transaction.Transaction.COD_3'),('DailyLimit.Account.AOIU_4', 'InterestEstimation.Account.AOIS_1', 'Transaction.Transaction.COD_2'),('DailyLimit.Account.COD_1', 'InterestEstimation.Account.AOIS_1', 'Transaction.Transaction.AOIU_1'),('DailyLimit.Account.COD_1', 'InterestEstimation.Account.AOIS_1', 'Transaction.Transaction.COD_1'),('DailyLimit.Account.COD_1', 'InterestEstimation.Account.AOIS_1', 'Transaction.Transaction.COD_3'),('DailyLimit.Account.COD_1', 'InterestEstimation.Account.AOIS_1', 'Transaction.Transaction.COD_2'),('DailyLimit.Account.COD_2', 'Lock.Account.COI_3', 'Transaction.Transaction.COD_2'),('DailyLimit.Account.AOIU_2', 'Lock.Account.COI_3', 'Transaction.Transaction.AOIU_1'),('DailyLimit.Account.AOIU_1', 'Lock.Account.COI_3', 'Transaction.Transaction.COD_1'),('DailyLimit.Account.AOIU_1', 'Lock.Account.COI_3', 'Transaction.Transaction.COD_2'),('DailyLimit.Account.AOIU_3', 'Lock.Account.COI_3', 'Transaction.Transaction.COD_2'),('Interest.Account.LOI_1', 'InterestEstimation.Account.AOIS_1', 'Transaction.Transaction.AOIU_1'),('Interest.Account.LOI_1', 'InterestEstimation.Account.AOIS_1', 'Transaction.Transaction.COD_3'),('Interest.Account.LOI_1', 'InterestEstimation.Account.AOIS_1', 'Transaction.Transaction.COD_2'),('Interest.Account.LOI_1', 'Lock.Account.COI_3', 'Transaction.Transaction.AOIU_1'),('Interest.Account.LOI_1', 'Lock.Account.COI_3', 'Transaction.Transaction.COD_1'),('InterestEstimation.Account.AOIS_1', 'Lock.Account.COI_3', 'Transaction.Transaction.AOIU_1'),('InterestEstimation.Account.AOIS_1', 'Lock.Account.COI_3', 'Transaction.Transaction.COD_1'),('InterestEstimation.Account.AOIS_1', 'Lock.Account.COI_3', 'Transaction.Transaction.COD_3'),('BankAccount.Account.AOIU_1', 'CreditWorthiness.Account.AOIU_1', 'Transaction.Transaction.AOIU_1'),('BankAccount.Account.AOIU_1', 'CreditWorthiness.Account.AOIU_1', 'Transaction.Transaction.COD_2'),('BankAccount.Account.AOIU_4', 'DailyLimit.Account.AOIS_42', 'Interest.Account.LOI_1'),('BankAccount.Account.AOIU_4', 'DailyLimit.Account.COD_2', 'Interest.Account.LOI_1'),('BankAccount.Account.AOIU_4', 'DailyLimit.Account.AOIU_2', 'Interest.Account.LOI_1'),('BankAccount.Account.AOIU_4', 'DailyLimit.Account.AOIU_1', 'Interest.Account.LOI_1'),('BankAccount.Account.AOIU_5', 'DailyLimit.Account.AOIU_2', 'Interest.Account.LOI_1'),('BankAccount.Account.AOIU_5', 'DailyLimit.Account.AOIU_1', 'Interest.Account.LOI_1'),('BankAccount.Account.AOIU_5', 'DailyLimit.Account.AOIU_4', 'Interest.Account.LOI_1'),('BankAccount.Account.AOIU_5', 'DailyLimit.Account.COD_1', 'Interest.Account.LOI_1'),('BankAccount.Account.AOIU_1', 'CreditWorthiness.Account.AOIU_1', 'DailyLimit.Account.AOIU_6'),('BankAccount.Account.AOIU_1', 'CreditWorthiness.Account.AOIU_1', 'DailyLimit.Account.AOIU_3'),('BankAccount.Account.AOIU_8', 'DailyLimit.Account.AOIU_7', 'InterestEstimation.Account.AOIS_1'),('BankAccount.Account.AOIU_5', 'DailyLimit.Account.AOIU_7', 'InterestEstimation.Account.AOIS_1'),('BankAccount.Account.AOIU_3', 'DailyLimit.Account.AOIU_7', 'InterestEstimation.Account.AOIS_1'),('BankAccount.Account.AOIU_7', 'DailyLimit.Account.AOIU_6', 'Lock.Account.COI_3')]
    # ------ END CONFIG ------

    project_dir = get_project_dir(project_name, base_dir)
    config_output_paths = ConfigManager.get_config_paths(project_dir, sort=True)
    variant_dirs = get_all_variant_dirs(project_dir, sort=True)
    # generate mutants and inject them to "optional" features
    if bug_ids:
        mutated_project_dirs = MutantManager.regenerate_filtered_mutants_from_bug_ids(project_dir, bug_ids,
                                                                                      num_of_bugs=num_of_seeding_bugs,
                                                                                      case_limit=case_limit)
    elif bug_tuples:
        mutated_project_dirs = MutantManager.regenerate_filtered_mutants_from_bug_tuples(project_dir, bug_tuples)
    else:
        raise Exception("Invalid bug input options")

    # compile mutated feature's source code
    for mutated_project_dir in mutated_project_dirs:
        for config_path, variant_dir in zip(config_output_paths, variant_dirs):
            mutated_variant_dir = VariantComposer.compose_by_config(mutated_project_dir, config_path)
            TestManager.link_generated_junit_test_cases(variant_dir, mutated_variant_dir)

        ConfigManager.copy_configs_report(project_dir, mutated_project_dir)

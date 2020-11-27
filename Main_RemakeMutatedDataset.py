import MutantManager
import ConfigManager
import TestManager
import VariantComposer

from FileManager import get_project_dir, get_all_variants_dirs

if __name__ == "__main__":
    # ------ START CONFIG ------
    base_dir = "/Users/tuanngokien/Desktop/Software_Analysis/configurable_system/dataset/"
    project_name = "4wise-BankAccountTP"
    num_of_seeding_bugs = 2
    bug_ids = ["CreditWorthiness.Account.AOIU_1","DailyLimit.Account.AOIU_4","DailyLimit.Account.AOIU_10","DailyLimit.Account.AOIU_2","DailyLimit.Account.AOIU_7","DailyLimit.Account.ROR_26","DailyLimit.Account.ROR_19","DailyLimit.Account.LOI_1","DailyLimit.Account.COD_1","DailyLimit.Account.AOIU_9","DailyLimit.Account.AOIU_3","DailyLimit.Account.AOIU_8","DailyLimit.Account.AOIU_5","DailyLimit.Account.ASRS_8","DailyLimit.Account.AOIS_4","DailyLimit.Account.COD_2","DailyLimit.Account.AOIS_8","DailyLimit.Account.AOIS_10"]
    # ------ END CONFIG ------

    project_dir = get_project_dir(project_name, base_dir)
    config_output_paths = ConfigManager.get_config_paths(project_dir, sort=True)
    variant_dirs = get_all_variants_dirs(project_dir, sort=True)

    # generate mutants and inject them to "optional" features
    mutated_project_dirs = MutantManager.regenerate_filtered_mutants(project_dir, bug_ids,
                                                                     num_of_bugs=num_of_seeding_bugs)

    # compile mutated feature's source code
    for mutated_project_dir in mutated_project_dirs:
        for config_path, variant_dir in zip(config_output_paths, variant_dirs):
            mutated_variant_dir = VariantComposer.compose_by_config(mutated_project_dir, config_path)
            TestManager.link_generated_junit_test_cases(variant_dir, mutated_variant_dir)

        ConfigManager.copy_configs_report(project_dir, mutated_project_dir)

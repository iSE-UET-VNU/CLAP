import MutantManager
import ConfigManager
import TestManager
import VariantComposer

from FileManager import get_project_dir, get_all_variants_dirs

if __name__ == "__main__":
    # ------ START CONFIG ------
    base_dir = None
    project_name = "2wise-Email-FH-JML-MB-Full"
    bug_ids = ["Base.EmailSystem.Util.AOIU_1", "Decrypt.EmailSystem.Client.AOIU_1", "Encrypt.EmailSystem.Client.AOIU_1", "Sign.EmailSystem.Client.AOIU_1", "Sign.EmailSystem.Email.ODL_1", "Verify.EmailSystem.Client.AOIS_1", "Verify.EmailSystem.Email.ODL_1"]
    # ------ END CONFIG ------

    project_dir = get_project_dir(project_name, base_dir)
    config_output_paths = ConfigManager.get_config_paths(project_dir, sort=True)
    variant_dirs = get_all_variants_dirs(project_dir, sort=True)

    # generate mutants and inject them to "optional" features
    mutated_project_dirs = MutantManager.regenerate_filtered_mutants(project_dir, bug_ids)

    # compile mutated feature's source code
    for mutated_project_dir in mutated_project_dirs:
        for config_path, variant_dir in zip(config_output_paths, variant_dirs):
            mutated_variant_dir = VariantComposer.compose_by_config(mutated_project_dir, config_path)
            TestManager.link_generated_junit_test_cases(variant_dir, mutated_variant_dir)

        ConfigManager.copy_configs_report(project_dir, mutated_project_dir)

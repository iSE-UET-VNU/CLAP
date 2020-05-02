from FileManager import get_project_dir, get_variant_dir, get_test_coverage_dir
import MutantManager
import RankingManager

if __name__ == "__main__":
    project_name = "Mutated-GPL-Test"
    project_dir = get_project_dir(project_name)
    mutated_project_name = "Trangnt_Test_Ranking"
    mutated_project_dir = MutantManager.get_mutated_project_dir(project_dir, mutated_project_name)

    variant_name = "model_01"
    variant_dir = get_variant_dir(mutated_project_dir, variant_name)

    test_coverage_dir = get_test_coverage_dir(variant_dir)

    suspicious_stms_list = {'GPL.Main.1': {'num_interactions': 1}, 'GPL.Main.3': {'num_interactions': 2},
                            'GPL.Test.1': {'num_interactions': 3}, 'GPL.Test.10': {'num_interactions': 3}}

    RankingManager.suspiciousness_calculation(test_coverage_dir, suspicious_stms_list)

    spectrum_ranked_list = RankingManager.spectrum_ranking()
    spc_spectrum_ranked_list = RankingManager.spc_spectrum_ranking()
    spc_interaction_spectrum_ranked_list = RankingManager.spc_interaction_spectrum_raking()

    buggy_statement = "TestProg.GPL.Main.6"
    print("spectrum ranking: ", RankingManager.search_rank(buggy_statement, spectrum_ranked_list))
    print("spc and spectrum ranking: ", RankingManager.search_rank(buggy_statement, spc_spectrum_ranked_list))
    print("spc, interaction and spectrum ranking: ", RankingManager.search_rank(buggy_statement, spc_interaction_spectrum_ranked_list))
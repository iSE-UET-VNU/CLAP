from FileManager import get_project_dir, get_variant_dir, get_test_coverage_dir
import MutantManager
import RankingManager

if __name__ == "__main__":
    project_name = "Mutated-GPL-Test"
    project_dir = get_project_dir(project_name)
    mutated_project_name = "BFS.GPL.Graph.COD_1"
    mutated_project_dir = MutantManager.get_mutated_project_dir(project_dir, mutated_project_name)

    suspicious_stms_list = {"BFS.GPL.Graph.25":{"num_interactions":2}, "BFS.GPL.Graph.1":{"num_interactions":1}, "BFS.GPL.Graph.12":{"num_interactions":4}, "BFS.GPL.Graph.13":{"num_interactions":5}}

    RankingManager.suspiciousness_calculation(mutated_project_dir, suspicious_stms_list)

    spectrum_ranked_list = RankingManager.spectrum_ranking()
    print(spectrum_ranked_list)
    spc_spectrum_ranked_list = RankingManager.spc_spectrum_ranking()
    spc_interaction_spectrum_ranked_list = RankingManager.spc_interaction_spectrum_raking()


    buggy_statement = "BFS.GPL.Graph.25"
    print("spectrum ranking: ", RankingManager.search_rank(buggy_statement, spectrum_ranked_list))
    print("spc and spectrum ranking: ", RankingManager.search_rank(buggy_statement, spc_spectrum_ranked_list))
    print("spc, interaction and spectrum ranking: ", RankingManager.search_rank(buggy_statement, spc_interaction_spectrum_ranked_list))


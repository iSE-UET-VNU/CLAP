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
    case_limit = 70
    bug_ids = ["Cycle.GPL.CycleWorkSpace.LOI_10","StronglyConnected.GPL.WorkSpaceTranspose.AOIS_1","Connected.GPL.RegionWorkSpace.AOIS_1","WeightedWithEdges.GPL.Edge.AOIS_10","UndirectedWithEdges.GPL.Edge.ROR_1","WeightedWithNeighbors.GPL.Neighbor.AOIS_7","Cycle.GPL.CycleWorkSpace.LOI_2","Cycle.GPL.Graph.ODL_1","Cycle.GPL.CycleWorkSpace.AORS_1","Cycle.GPL.CycleWorkSpace.AORS_3","WeightedOnlyVertices.GPL.Vertex.AOIU_6","WeightedWithEdges.GPL.Edge.AOIU_1","Cycle.GPL.CycleWorkSpace.COI_7","Cycle.GPL.CycleWorkSpace.COI_13","Number.GPL.NumberWorkSpace.CDL_1","Cycle.GPL.CycleWorkSpace.LOI_3","Cycle.GPL.CycleWorkSpace.AOIU_4","WeightedOnlyVertices.GPL.Vertex.AORS_1","WeightedOnlyVertices.GPL.Vertex.LOI_2","WeightedWithNeighbors.GPL.Neighbor.AOIU_3","Number.GPL.NumberWorkSpace.AODS_1","WeightedOnlyVertices.GPL.Graph.ODL_2","DirectedWithEdges.GPL.Edge.ROR_2","Connected.GPL.RegionWorkSpace.AOIU_1","StronglyConnected.GPL.FinishTimeWorkSpace.AORS_3","Cycle.GPL.CycleWorkSpace.CDL_2","Cycle.GPL.CycleWorkSpace.ROR_1","WeightedWithNeighbors.GPL.Graph.AOIU_1","MSTKruskal.GPL.Vertex.ROR_1","Cycle.GPL.CycleWorkSpace.ODL_18","Cycle.GPL.CycleWorkSpace.ODL_16","Cycle.GPL.CycleWorkSpace.COR_2","WeightedWithNeighbors.GPL.Neighbor.LOI_1","Cycle.GPL.Graph.COI_1","Cycle.GPL.CycleWorkSpace.AOIU_1","BFS.GPL.Graph.CDL_1","Cycle.GPL.CycleWorkSpace.COI_3","UndirectedWithEdges.GPL.Edge.ODL_5","Cycle.GPL.CycleWorkSpace.AOIU_3","UndirectedWithNeighbors.GPL.Neighbor.ODL_2","Cycle.GPL.CycleWorkSpace.COI_12","WeightedWithNeighbors.GPL.Neighbor.AOIU_2","BFS.GPL.Graph.COD_1","StronglyConnected.GPL.FinishTimeWorkSpace.ROR_1","Cycle.GPL.CycleWorkSpace.AORS_4","Number.GPL.NumberWorkSpace.LOI_1","WeightedWithEdges.GPL.Edge.AOIS_1","WeightedWithNeighbors.GPL.Neighbor.AOIS_15","Connected.GPL.RegionWorkSpace.AODU_1","Cycle.GPL.Vertex.AOIS_1","Cycle.GPL.CycleWorkSpace.ODL_10","DirectedWithEdges.GPL.Edge.ODL_9","WeightedWithEdges.GPL.Edge.AOIU_2","Cycle.GPL.CycleWorkSpace.COI_5","WeightedWithNeighbors.GPL.Vertex.AOIS_5","Cycle.GPL.CycleWorkSpace.ROR_2","WeightedWithEdges.GPL.Edge.AOIS_11","WeightedWithNeighbors.GPL.Neighbor.AOIU_4","WeightedWithNeighbors.GPL.Vertex.AOIU_1","WeightedOnlyVertices.GPL.Vertex.AOIS_17","Cycle.GPL.CycleWorkSpace.COR_3","Cycle.GPL.CycleWorkSpace.ODL_21","Cycle.GPL.CycleWorkSpace.COI_11","UndirectedWithEdges.GPL.Edge.COI_2","Cycle.GPL.CycleWorkSpace.LOI_7","DirectedWithEdges.GPL.Edge.ROR_1","Connected.GPL.RegionWorkSpace.AORS_1","Number.GPL.NumberWorkSpace.AORS_2","Cycle.GPL.CycleWorkSpace.ODL_15","Cycle.GPL.CycleWorkSpace.COI_8","WeightedWithEdges.GPL.Edge.AOIS_5","WeightedWithEdges.GPL.Edge.AOIU_3","Number.GPL.NumberWorkSpace.ODL_2","UndirectedWithEdges.GPL.Edge.ODL_9","WeightedWithNeighbors.GPL.Graph.LOI_1","DFS.GPL.Graph.ODL_1","WeightedWithNeighbors.GPL.Graph.ROR_1","Connected.GPL.RegionWorkSpace.AOIS_3","WeightedWithNeighbors.GPL.Vertex.AOIS_1","StronglyConnected.GPL.FinishTimeWorkSpace.ODL_2","Cycle.GPL.CycleWorkSpace.COR_1","DirectedWithNeighbors.GPL.Neighbor.ODL_2","Cycle.GPL.CycleWorkSpace.ODL_9","WeightedWithNeighbors.GPL.Neighbor.AOIU_1","Cycle.GPL.CycleWorkSpace.ODL_2","WeightedWithNeighbors.GPL.Neighbor.AOIS_11","DFS.GPL.Graph.COD_1","WeightedOnlyVertices.GPL.Graph.CDL_1","WeightedOnlyVertices.GPL.Vertex.ODL_5","StronglyConnected.GPL.FinishTimeWorkSpace.AODS_2","Cycle.GPL.CycleWorkSpace.ODL_22","StronglyConnected.GPL.FinishTimeWorkSpace.AORS_1"]
    # ------ END CONFIG ------

    project_dir = get_project_dir(project_name, base_dir)
    config_output_paths = ConfigManager.get_config_paths(project_dir, sort=True)
    variant_dirs = get_all_variants_dirs(project_dir, sort=True)

    # generate mutants and inject them to "optional" features
    mutated_project_dirs = MutantManager.regenerate_filtered_mutants(project_dir, bug_ids,
                                                                     num_of_bugs=num_of_seeding_bugs, case_limit=case_limit)

    # compile mutated feature's source code
    for mutated_project_dir in mutated_project_dirs:
        for config_path, variant_dir in zip(config_output_paths, variant_dirs):
            mutated_variant_dir = VariantComposer.compose_by_config(mutated_project_dir, config_path)
            TestManager.link_generated_junit_test_cases(variant_dir, mutated_variant_dir)

        ConfigManager.copy_configs_report(project_dir, mutated_project_dir)

import AntManager
import InvolvingFeatureManager
import MutantManager
import TestManager

from FileManager import get_project_dir, lock_project
from Helpers import sleep, natural_sort
from VariantComposer import was_variants_composed

if __name__ == "__main__":

    # ------ START CONFIG ------
    base_dir = "/Users/tuanngokien/Desktop/Software_Analysis/configurable_system/dataset/"
    project_name = "4wise-Elevator-FH-JML-IF-Lite"
    project_dir = get_project_dir(project_name, base_dir)
    # ------ END CONFIG ------

    mutated_project_dirs = MutantManager.get_mutated_project_dirs(project_dir, sort=True)
    for mutated_project_dir in mutated_project_dirs:
        InvolvingFeatureManager.summarize_involving_features(project_dir, mutated_project_dir)
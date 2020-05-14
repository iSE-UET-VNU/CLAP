import TestManager

from FileManager import get_project_dir, get_variant_dir

if __name__ == "__main__":
    project_name = "Elevator-FH-JML"
    project_dir = get_project_dir(project_name)
    variant_name = "model_m_ca3_0001"

    variant_dir = get_variant_dir(project_dir, variant_name)
    # TestManager.run_junit_test_cases_with_coverage(variant_dir, halt_on_failure=True, halt_on_error=True)
    TestManager.link_generated_junit_test_cases(variant_dir, "/Users/tuanngokien/Desktop/Software_Analysis/configurable_system/InputPreparation/projects/Elevator-FH-JML/mutated")

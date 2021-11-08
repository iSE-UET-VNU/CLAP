from DDU.DDU import *
from FileManager import join_path, list_dir
from label_data.HelperForLabeledData import *

labels = [FAILING, FALSE_PASSING, TRUE_PASSING]
count_for_labels = ["Count_" + FAILING, "Count_" + FALSE_PASSING, "Count_" + TRUE_PASSING]

if __name__ == "__main__":
    system_dir = "/Users/thu-trangnguyen/Documents/Research/SPL/Debug/1Bug/4wise/"
    mutated_projects = list_dir(system_dir)
    average_ddu = {}
    sytem_name = "ZipMe"
    for project in mutated_projects:
        project_dir = join_path(system_dir, project)
        variants_and_labels = get_variants_and_labels(project_dir)
        variants_dir = get_variants_dir(project_dir)
        sum_ddu  = {}
        count_ddu = {}
        for variant in variants_and_labels:
            var_dir = join_path(variants_dir, variant)
            var_ddu = ddu(var_dir, variants_and_labels[variant][LABEL])
            variants_and_labels[variant][DDU] = var_ddu
            if(variants_and_labels[variant][LABEL] not in sum_ddu):
                sum_ddu[variants_and_labels[variant][LABEL]] = 0
                count_ddu[variants_and_labels[variant][LABEL]] = 0
            sum_ddu[variants_and_labels[variant][LABEL]] += var_ddu
            count_ddu[variants_and_labels[variant][LABEL]] += 1
        average_ddu[project] = {}
        for l in labels:
            average_ddu[project][l] = sum_ddu[l]/count_ddu[l]
        for l in labels:
            average_ddu[project]["Count_" + l] = count_ddu[l]
        write_dict_to_file(join_path(project_dir,"ddu_info.csv"), variants_and_labels, [VARIANT_NAME, LABEL, CREATED_FP, DDU])

    write_dict_to_file(join_path("/Users/thu-trangnguyen/Documents/Projects/VarCop/experiment_results/Consistent_Testing", sytem_name + "_ddu_1Bug.csv"),
                       average_ddu,
                       ["PROJECT ID", FAILING, FALSE_PASSING, TRUE_PASSING, "Count_" + FAILING, "Count_" + FALSE_PASSING, "Count_" + TRUE_PASSING])

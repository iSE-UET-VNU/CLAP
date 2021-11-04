from label_data.LabelData import *


if __name__ == "__main__":
    project_base_path = "/Users/thu-trangnguyen/Documents/Research/SPL/GPL/1Bug/1wise"
    base_features = ["Base"]
    mutated_projects_list = list_dir(project_base_path)
    bugs_in_bases = []
    one_fail = []
    buggy_features_but_not_buggy_stmts = []
    for mutated_project in mutated_projects_list:
        mu_project_path = join_path(project_base_path, mutated_project)
        buggy_stmts = get_multiple_buggy_statements(mutated_project, mu_project_path)
        buggy_features = get_mutated_features(mu_project_path)
        config_report_path = get_model_configs_report_path(mu_project_path)
        failing_variants = get_failing_variants(mu_project_path)

        if base_is_buggy_features(base_features, buggy_features):
            bugs_in_bases.append(mutated_project)
        else:
            passing_variants_contain_buggy_features = passing_product_has_buggy_features(config_report_path,
                                                                                         buggy_features)
            # if len(passing_variants_contain_buggy_features) == 0:
            #    print("trang")
            # else:
            passing_variants_contain_buggy_stmts = passing_product_has_buggy_statements(mu_project_path,
                                                                                        passing_variants_contain_buggy_features,
                                                                                        buggy_stmts)
            # if len(passing_variants_contain_buggy_stmts) > 0:
            if len(passing_variants_contain_buggy_features) > 0 and len(passing_variants_contain_buggy_stmts) == 0 and len(failing_variants) != 1:
                buggy_features_but_not_buggy_stmts.append(mutated_project)
            if len(failing_variants) == 1 and len(passing_variants_contain_buggy_stmts) == 0:
                one_fail.append(mutated_project)
            else:
                #print(mutated_project)
                label(mu_project_path, passing_variants_contain_buggy_stmts)

    print("bugs in base")
    for item in bugs_in_bases:
        print(item)
    print("-----")
    print("one fails")
    for item in one_fail:
        print(item)
    print("----")
    print("features but not stmts")
    for item in buggy_features_but_not_buggy_stmts:
        print(item)

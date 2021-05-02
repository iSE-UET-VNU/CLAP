import logging
import os
import xml.etree.ElementTree as ET

from FileManager import get_all_variant_dirs, get_test_coverage_dir, \
    get_spectrum_failed_coverage_file_name_with_version, get_spectrum_passed_coverage_file_name_with_version, join_path

from ranking.Spectrum_Expression import TARANTULA, tarantula_calculation, OCHIAI, ochiai_calculation, OP2, \
    op2_calculation, BARINEL, DSTAR, barinel_calculation, dstar_calculation, RUSSELL_RAO, russell_rao_calculation, \
    SIMPLE_MATCHING, simple_matching_calculation, ROGERS_TANIMOTO, rogers_tanimoto_calculation, AMPLE, \
    ample_calculation, JACCARD, jaccard_calculation, COHEN, cohen_calculation, SCOTT, scott_calculation, ROGOT1, \
    rogot1_calculation, GEOMETRIC_MEAN, geometric_mean_calculation, M2, m2_calculation, WONG1, wong1_calculation, SOKAL, \
    sokal_calculation, SORENSEN_DICE, sorensen_dice_calculation, DICE, dice_calculation, HUMANN, humman_calculation, M1, \
    m1_calculation, WONG2, WONG3, wong2_calculation, wong3_calculation, ZOLTAR, OVERLAP, zoltar_calculation, \
    overlap_calculation, EUCLID, euclid_calculation, ROGOT2, rogot2_calculation, HAMMING, hamming_calculation, FLEISS, \
    fleiss_calculation, ANDERBERG, anderberg_calculation, GOODMAN, goodman_calculation, HARMONIC_MEAN, \
    harmonic_mean_calculation, KULCZYNSKI1, kulczynski1_calculation, KULCZYNSKI2, kulczynski2_calculation

VARIANT_LEVEL_SUSPICIOUSNESS_SCORE = "variant_level_suspiciousness_score"

def init_num_of_failing_passing_variants(list_of_stms):
    data = {}
    for stm in list_of_stms:
        data[stm] = {}
        data[stm]["num_of_passing"] = 0
        data[stm]["num_of_failing"] = 0
    return data


def read_data_from_coverage_file(data, coverage_file, variant_type):
    try:
        tree = ET.parse(coverage_file)
        root = tree.getroot()
        project = root.find("project")
        check_duplicate = []
        for package in project:
            for file in package:
                for line in file:
                    id = line.get('featureClass') + "." + line.get('featureLineNum')
                    if id not in data:
                        data[id] = {}
                        data[id]["num_of_failing"] = 0
                        data[id]["num_of_passing"] = 0

                    if int(line.get('count')) > 0:
                        if id not in check_duplicate:
                            data[id][variant_type] += 1
                            check_duplicate.append(id)
        return data
    except:
        logging.info("Exception when parsing %s", coverage_file)


def get_num_passing_failing_variants(mutated_project_dir, list_of_stms, spectrum_coverage_prefix):

    failing_passing_variants_of_stms = init_num_of_failing_passing_variants(list_of_stms)
    variants_list = get_all_variant_dirs(mutated_project_dir)
    total_fails = 0
    total_passes = 0
    for variant_dir in variants_list:
        test_coverage_dir = get_test_coverage_dir(variant_dir)
        spectrum_failed_file = get_spectrum_failed_coverage_file_name_with_version(spectrum_coverage_prefix)
        spectrum_failed_coverage_file_dir = join_path(test_coverage_dir, spectrum_failed_file)
        spectrum_passed_file = get_spectrum_passed_coverage_file_name_with_version(spectrum_coverage_prefix)
        spectrum_passed_coverage_file_dir = join_path(test_coverage_dir, spectrum_passed_file)

        if os.path.isfile(spectrum_failed_coverage_file_dir):
            failing_passing_variants_of_stms = read_data_from_coverage_file(failing_passing_variants_of_stms,
                                                                    spectrum_failed_coverage_file_dir,
                                                                    "num_of_failing")
            total_fails += 1
        if not os.path.isfile(spectrum_failed_coverage_file_dir) and os.path.isfile(spectrum_passed_coverage_file_dir):
            failing_passing_variants_of_stms = read_data_from_coverage_file(failing_passing_variants_of_stms,
                                                                    spectrum_passed_coverage_file_dir,
                                                                    "num_of_passing")
            total_passes += 1
    return failing_passing_variants_of_stms, total_fails, total_passes


def calculate_suspiciousness_variant_level(failing_passing_variants_of_stms, total_fails, total_passes, spectrum_expression):
    for stm in failing_passing_variants_of_stms.keys():
        failing_passing_variants_of_stms[stm][VARIANT_LEVEL_SUSPICIOUSNESS_SCORE] = tarantula_calculation(failing_passing_variants_of_stms[stm]["num_of_failing"],
                                                                                                      failing_passing_variants_of_stms[stm]["num_of_passing"],
                                                                                                      total_fails, total_passes)

        if spectrum_expression == TARANTULA:
            failing_passing_variants_of_stms[stm][VARIANT_LEVEL_SUSPICIOUSNESS_SCORE] = tarantula_calculation(
                failing_passing_variants_of_stms[stm]["num_of_failing"],
                failing_passing_variants_of_stms[stm]["num_of_passing"],
                total_fails, total_passes)
            if(stm == "DailyLimit.Account.19"  or stm == "DailyLimit.Account.35"):
                print("variant level")
                print(stm, "  ", failing_passing_variants_of_stms[stm]["num_of_failing"], "   ", failing_passing_variants_of_stms[stm]["num_of_passing"],
                      "    ", total_fails, "      ", total_passes, "     ", failing_passing_variants_of_stms[stm][VARIANT_LEVEL_SUSPICIOUSNESS_SCORE])

        elif spectrum_expression == OCHIAI:
            failing_passing_variants_of_stms[stm][VARIANT_LEVEL_SUSPICIOUSNESS_SCORE] = ochiai_calculation(
                failing_passing_variants_of_stms[stm]["num_of_failing"],
                failing_passing_variants_of_stms[stm]["num_of_passing"],
                total_fails, total_passes)

        elif spectrum_expression == OP2:
            failing_passing_variants_of_stms[stm][VARIANT_LEVEL_SUSPICIOUSNESS_SCORE] = op2_calculation(
                failing_passing_variants_of_stms[stm]["num_of_failing"],
                failing_passing_variants_of_stms[stm]["num_of_passing"],
                total_fails, total_passes)
            if(stm == "Base.ElevatorSystem.Elevator.57"  or stm == "Weight.ElevatorSystem.Elevator.32"):
                print("variant level")
                print(stm, "  ", failing_passing_variants_of_stms[stm]["num_of_failing"], "   ", failing_passing_variants_of_stms[stm]["num_of_passing"],
                      "    ", total_fails, "      ", total_passes, "     ", failing_passing_variants_of_stms[stm][VARIANT_LEVEL_SUSPICIOUSNESS_SCORE])

        elif spectrum_expression == BARINEL:
            failing_passing_variants_of_stms[stm][VARIANT_LEVEL_SUSPICIOUSNESS_SCORE] = barinel_calculation(
                failing_passing_variants_of_stms[stm]["num_of_failing"],
                failing_passing_variants_of_stms[stm]["num_of_passing"],
                total_fails, total_passes)

        elif spectrum_expression == DSTAR:
            failing_passing_variants_of_stms[stm][VARIANT_LEVEL_SUSPICIOUSNESS_SCORE] = dstar_calculation(
                failing_passing_variants_of_stms[stm]["num_of_failing"],
                failing_passing_variants_of_stms[stm]["num_of_passing"],
                total_fails, total_passes)

        elif spectrum_expression == RUSSELL_RAO:
            failing_passing_variants_of_stms[stm][VARIANT_LEVEL_SUSPICIOUSNESS_SCORE] = russell_rao_calculation(
                failing_passing_variants_of_stms[stm]["num_of_failing"],
                failing_passing_variants_of_stms[stm]["num_of_passing"],
                total_fails, total_passes)

        elif spectrum_expression == SIMPLE_MATCHING:
            failing_passing_variants_of_stms[stm][VARIANT_LEVEL_SUSPICIOUSNESS_SCORE] = simple_matching_calculation(
                failing_passing_variants_of_stms[stm]["num_of_failing"],
                failing_passing_variants_of_stms[stm]["num_of_passing"],
                total_fails, total_passes)

        elif spectrum_expression == ROGERS_TANIMOTO:
            failing_passing_variants_of_stms[stm][VARIANT_LEVEL_SUSPICIOUSNESS_SCORE] = rogers_tanimoto_calculation(
                failing_passing_variants_of_stms[stm]["num_of_failing"],
                failing_passing_variants_of_stms[stm]["num_of_passing"],
                total_fails, total_passes)

        elif spectrum_expression == AMPLE:
            failing_passing_variants_of_stms[stm][VARIANT_LEVEL_SUSPICIOUSNESS_SCORE] = ample_calculation(
                failing_passing_variants_of_stms[stm]["num_of_failing"],
                failing_passing_variants_of_stms[stm]["num_of_passing"],
                total_fails, total_passes)

        elif spectrum_expression == JACCARD:
            failing_passing_variants_of_stms[stm][VARIANT_LEVEL_SUSPICIOUSNESS_SCORE] = jaccard_calculation(
                failing_passing_variants_of_stms[stm]["num_of_failing"],
                failing_passing_variants_of_stms[stm]["num_of_passing"],
                total_fails, total_passes)

        elif spectrum_expression == COHEN:
            failing_passing_variants_of_stms[stm][VARIANT_LEVEL_SUSPICIOUSNESS_SCORE] = cohen_calculation(
                failing_passing_variants_of_stms[stm]["num_of_failing"],
                failing_passing_variants_of_stms[stm]["num_of_passing"],
                total_fails, total_passes)

        elif spectrum_expression == SCOTT:
            failing_passing_variants_of_stms[stm][VARIANT_LEVEL_SUSPICIOUSNESS_SCORE] = scott_calculation(
                failing_passing_variants_of_stms[stm]["num_of_failing"],
                failing_passing_variants_of_stms[stm]["num_of_passing"],
                total_fails, total_passes)

        elif spectrum_expression == ROGOT1:
            failing_passing_variants_of_stms[stm][VARIANT_LEVEL_SUSPICIOUSNESS_SCORE] = rogot1_calculation(
                failing_passing_variants_of_stms[stm]["num_of_failing"],
                failing_passing_variants_of_stms[stm]["num_of_passing"],
                total_fails, total_passes)

        elif spectrum_expression == GEOMETRIC_MEAN:
            failing_passing_variants_of_stms[stm][VARIANT_LEVEL_SUSPICIOUSNESS_SCORE] = geometric_mean_calculation(
                failing_passing_variants_of_stms[stm]["num_of_failing"],
                failing_passing_variants_of_stms[stm]["num_of_passing"],
                total_fails, total_passes)

        elif spectrum_expression == M2:
            failing_passing_variants_of_stms[stm][VARIANT_LEVEL_SUSPICIOUSNESS_SCORE] = m2_calculation(
                failing_passing_variants_of_stms[stm]["num_of_failing"],
                failing_passing_variants_of_stms[stm]["num_of_passing"],
                total_fails, total_passes)

        elif spectrum_expression == WONG1:
            failing_passing_variants_of_stms[stm][VARIANT_LEVEL_SUSPICIOUSNESS_SCORE] = wong1_calculation(
                failing_passing_variants_of_stms[stm]["num_of_failing"],
                failing_passing_variants_of_stms[stm]["num_of_passing"],
                total_fails, total_passes)

        elif spectrum_expression == SOKAL:
            failing_passing_variants_of_stms[stm][VARIANT_LEVEL_SUSPICIOUSNESS_SCORE] = sokal_calculation(
                failing_passing_variants_of_stms[stm]["num_of_failing"],
                failing_passing_variants_of_stms[stm]["num_of_passing"],
                total_fails, total_passes)

        # new
        elif spectrum_expression == SORENSEN_DICE:
            failing_passing_variants_of_stms[stm][VARIANT_LEVEL_SUSPICIOUSNESS_SCORE] = sorensen_dice_calculation(
                failing_passing_variants_of_stms[stm]["num_of_failing"],
                failing_passing_variants_of_stms[stm]["num_of_passing"],
                total_fails, total_passes)

        elif spectrum_expression == DICE:
            failing_passing_variants_of_stms[stm][VARIANT_LEVEL_SUSPICIOUSNESS_SCORE] = dice_calculation(
                failing_passing_variants_of_stms[stm]["num_of_failing"],
                failing_passing_variants_of_stms[stm]["num_of_passing"],
                total_fails, total_passes)

        elif spectrum_expression == HUMANN:
            failing_passing_variants_of_stms[stm][VARIANT_LEVEL_SUSPICIOUSNESS_SCORE] = humman_calculation(
                failing_passing_variants_of_stms[stm]["num_of_failing"],
                failing_passing_variants_of_stms[stm]["num_of_passing"],
                total_fails, total_passes)

        elif spectrum_expression == M1:
            failing_passing_variants_of_stms[stm][VARIANT_LEVEL_SUSPICIOUSNESS_SCORE] = m1_calculation(
                failing_passing_variants_of_stms[stm]["num_of_failing"],
                failing_passing_variants_of_stms[stm]["num_of_passing"],
                total_fails, total_passes)

        elif spectrum_expression == WONG2:
            failing_passing_variants_of_stms[stm][VARIANT_LEVEL_SUSPICIOUSNESS_SCORE] = wong2_calculation(
                failing_passing_variants_of_stms[stm]["num_of_failing"],
                failing_passing_variants_of_stms[stm]["num_of_passing"],
                total_fails, total_passes)

        elif spectrum_expression == WONG3:
            failing_passing_variants_of_stms[stm][VARIANT_LEVEL_SUSPICIOUSNESS_SCORE] = wong3_calculation(
                failing_passing_variants_of_stms[stm]["num_of_failing"],
                failing_passing_variants_of_stms[stm]["num_of_passing"],
                total_fails, total_passes)

        elif spectrum_expression == ZOLTAR:
            failing_passing_variants_of_stms[stm][VARIANT_LEVEL_SUSPICIOUSNESS_SCORE] = zoltar_calculation(
                failing_passing_variants_of_stms[stm]["num_of_failing"],
                failing_passing_variants_of_stms[stm]["num_of_passing"],
                total_fails, total_passes)

        elif spectrum_expression == OVERLAP:
            failing_passing_variants_of_stms[stm][VARIANT_LEVEL_SUSPICIOUSNESS_SCORE] = overlap_calculation(
                failing_passing_variants_of_stms[stm]["num_of_failing"],
                failing_passing_variants_of_stms[stm]["num_of_passing"],
                total_fails, total_passes)

        elif spectrum_expression == EUCLID:
            failing_passing_variants_of_stms[stm][VARIANT_LEVEL_SUSPICIOUSNESS_SCORE] = euclid_calculation(
                failing_passing_variants_of_stms[stm]["num_of_failing"],
                failing_passing_variants_of_stms[stm]["num_of_passing"],
                total_fails, total_passes)

        elif spectrum_expression == ROGOT2:
            failing_passing_variants_of_stms[stm][VARIANT_LEVEL_SUSPICIOUSNESS_SCORE] = rogot2_calculation(
                failing_passing_variants_of_stms[stm]["num_of_failing"],
                failing_passing_variants_of_stms[stm]["num_of_passing"],
                total_fails, total_passes)

        elif spectrum_expression == HAMMING:
            failing_passing_variants_of_stms[stm][VARIANT_LEVEL_SUSPICIOUSNESS_SCORE] = hamming_calculation(
                failing_passing_variants_of_stms[stm]["num_of_failing"],
                failing_passing_variants_of_stms[stm]["num_of_passing"],
                total_fails, total_passes)

        elif spectrum_expression == FLEISS:
            failing_passing_variants_of_stms[stm][VARIANT_LEVEL_SUSPICIOUSNESS_SCORE] = fleiss_calculation(
                failing_passing_variants_of_stms[stm]["num_of_failing"],
                failing_passing_variants_of_stms[stm]["num_of_passing"],
                total_fails, total_passes)

        elif spectrum_expression == ANDERBERG:
            failing_passing_variants_of_stms[stm][VARIANT_LEVEL_SUSPICIOUSNESS_SCORE] = anderberg_calculation(
                failing_passing_variants_of_stms[stm]["num_of_failing"],
                failing_passing_variants_of_stms[stm]["num_of_passing"],
                total_fails, total_passes)

        elif spectrum_expression == GOODMAN:
            failing_passing_variants_of_stms[stm][VARIANT_LEVEL_SUSPICIOUSNESS_SCORE] = goodman_calculation(
                failing_passing_variants_of_stms[stm]["num_of_failing"],
                failing_passing_variants_of_stms[stm]["num_of_passing"],
                total_fails, total_passes)

        elif spectrum_expression == HARMONIC_MEAN:
            failing_passing_variants_of_stms[stm][VARIANT_LEVEL_SUSPICIOUSNESS_SCORE] = harmonic_mean_calculation(
                failing_passing_variants_of_stms[stm]["num_of_failing"],
                failing_passing_variants_of_stms[stm]["num_of_passing"],
                total_fails, total_passes)

        elif spectrum_expression == KULCZYNSKI1:
            failing_passing_variants_of_stms[stm][VARIANT_LEVEL_SUSPICIOUSNESS_SCORE] = kulczynski1_calculation(
                failing_passing_variants_of_stms[stm]["num_of_failing"],
                failing_passing_variants_of_stms[stm]["num_of_passing"],
                total_fails, total_passes)

        elif spectrum_expression == KULCZYNSKI2:
            failing_passing_variants_of_stms[stm][VARIANT_LEVEL_SUSPICIOUSNESS_SCORE] = kulczynski2_calculation(
                failing_passing_variants_of_stms[stm]["num_of_failing"],
                failing_passing_variants_of_stms[stm]["num_of_passing"],
                total_fails, total_passes)

    return failing_passing_variants_of_stms
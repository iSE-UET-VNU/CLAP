import logging
import os
import xml.etree.ElementTree as ET
from FileManager import get_test_coverage_dir, join_path, SPECTRUM_PASSED_COVERAGE_FILE_NAME, get_variants_dir, list_dir


def statement_coverage(variant_dir):
    test_coverage_dir = get_test_coverage_dir(variant_dir)
    spectrum_passed_coverage_file = join_path(test_coverage_dir, SPECTRUM_PASSED_COVERAGE_FILE_NAME)
    num_of_stm = 0
    untested_stm = 0
    if os.path.isfile(spectrum_passed_coverage_file):
        try:
            tree = ET.parse(spectrum_passed_coverage_file)
            root = tree.getroot()
            project = root.find("project")
            for package in project:
                for file in package:
                    for line in file:
                        num_of_stm += 1
                        if (int(line.get("count")) == 0):
                            untested_stm += 1
        except:
            logging.info("Exception when parsing %s", spectrum_passed_coverage_file)
    else:
        logging.info("spectrum passed coveraged file does not exist in %s", variant_dir)

    coverage_rate = (num_of_stm - untested_stm) / num_of_stm
    return coverage_rate


def statement_coverage_of_variants(project_dir):
    stm_coverage_variants = {}
    variants_dir = get_variants_dir(project_dir)
    for variant in list_dir(variants_dir):
        variant_dir = join_path(variants_dir, variant)
        testing_coverage = statement_coverage(variant_dir)
        stm_coverage_variants[variant] = testing_coverage

    return stm_coverage_variants
import csv

from FileManager import *
from label_data.LabelData import *
from FileManager import *
import xml.etree.ElementTree as ET

ACTUAl_PASSING = "AP"
FALSE_PASSING = "FP"
FAILING = "F"
LABELED_FILE_NAME = "variants_testing_label.csv"

VARIANT_NAME = 'VARIANT'
LABEL = 'LABEL'
CREATED_FP = 'FP created from F'
DDU = "DDU"

def get_variants_and_labels(mutated_project_dir):
    variants = {}
    label_file = join_path(mutated_project_dir, LABELED_FILE_NAME)
    with open(label_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            variants[row[VARIANT_NAME]] = {LABEL: row[LABEL], CREATED_FP: row[CREATED_FP]}
    return variants


def write_dict_to_file(file_name, data, fieldnames):
    with open(file_name, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for item in data:
           tmp = {}
           for f in fieldnames:
               if fieldnames.index(f) == 0:
                   tmp[f] = item
               else:
                    tmp[f] = data[item][f]
           writer.writerow(tmp)


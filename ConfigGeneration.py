import csv
import re
from collections import defaultdict, OrderedDict
import xml.etree.ElementTree as ET
from xml.dom import minidom

from FileManager import get_model_config_dir, get_outer_dir, get_file_name, join_path
from Helpers import get_logger
import Model

logger = get_logger(__name__)


def get_optional_feature_names(sampling_file_path):
    optional_feature_names = []
    with open(sampling_file_path, "r") as input_file:
        csv_reader = csv.reader(input_file, delimiter=';')
        next(csv_reader)
        for row in csv_reader:
            label = re.sub("[\[\]\* ]", '', row[0])
            feature_statuses = row[2:-1]
            is_optional_feature = 0 < len(list(filter(lambda status: status == "X", feature_statuses))) < len(
                feature_statuses)
            if is_optional_feature:
                optional_feature_names.append(label)
    return optional_feature_names


def get_configurations_from_sampling_file(ordered_features, sampling_file_path):
    with open(sampling_file_path, "r") as input_file:
        csv_reader = csv.reader(input_file, delimiter=';')
        next(csv_reader)
        configurations = defaultdict(OrderedDict)
        sampling_matrix = list(csv_reader)
        sampling_matrix.sort(key=lambda row: ordered_features.index(row[0]))
        for row in sampling_matrix:
            label = re.sub("[\[\]\* ]", '', row[0])
            for i, feature_selection in enumerate(row[2:-1]):
                configurations[i][label] = feature_selection == "X"
    return configurations.values()


def write_configuration_to_file(configuration, output_file_path):
    lines = []
    for feature, is_enabled in configuration.items():
        # comment all disabled features
        line = ("" if is_enabled else "#") + feature
        lines.append(line)
    with open(output_file_path, "w+") as output_file:
        output_file.write("\n".join(lines))


def generate_configs(feature_order_file_path, sampling_output_file_path):
    logger.info(f"Generating configurations from sampling csv file [{get_file_name(sampling_output_file_path)}]")
    config_dir = get_model_config_dir(get_outer_dir(sampling_output_file_path))
    sampling_file_name = get_file_name(sampling_output_file_path).replace(".", "_")
    ordered_features = Model.read_feature_order_file(feature_order_file_path)
    configurations = get_configurations_from_sampling_file(ordered_features, sampling_output_file_path)
    config_output_paths = []
    for i, config in enumerate(configurations):
        config_output_path = join_path(config_dir, f"{sampling_file_name}_{str(i + 1).zfill(4)}.features")
        write_configuration_to_file(config, config_output_path)
        config_output_paths.append(config_output_path)
    return config_output_paths

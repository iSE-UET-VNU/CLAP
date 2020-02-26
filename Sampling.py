import re

from FileManager import get_plugin_path
from Helpers import get_logger, execute_shell_command

logger = get_logger(__name__)


def get_sampling_file_path(output_log):
    return re.search("(?<=Wrote result to )[^\r\n]+", output_log).group()


def sampling(model_file_path, t_wise):
    # todo SPLCA generate sampling contains abstract features
    #  -> generate duplicate variants which contribute by solely concrete features

    plugin_name = "SPLCATool.jar"
    plugin_path = get_plugin_path(plugin_name)
    logger.info(f"Running sampling for model file [{model_file_path}] with {t_wise}-wise")
    output_log = execute_shell_command(f'java -jar {plugin_path} ', extra_args=[
        {"-t": "t_wise"},
        {"-fm": model_file_path},
        {"-s": t_wise},

    ])
    return get_sampling_file_path(output_log)

import logging
import re
import subprocess
import hashlib
import time

from FileManager import get_log_file_path, remove_file

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s [%(levelname)s] [%(module)s] %(message)s",
                    datefmt='%Y-%m-%d %H:%M:%S')


def get_logger(name):
    return logging.getLogger(name)


logger = get_logger(__name__)


def hash_md5(input_str):
    return hashlib.md5(input_str.encode()).hexdigest()


def get_current_timestamp():
    return round(time.time())


def find_plugin_name(command):
    plugin_names = re.findall("[^ /]+\.jar", command)
    if len(plugin_names) > 0:
        return plugin_names[0]


def execute_shell_command(command, extra_args=None, show_log_path=False):
    if extra_args:
        for args in extra_args:
            assert isinstance(args, dict), """Input Argument must be passed as dict={"name":"value"}"""
            arg_name = list(args.keys())[0]
            arg_val = args.get(arg_name, "")
            command += f" {arg_name} {arg_val}"
    log_file_name = f"{get_current_timestamp()}_{hash_md5(command)}.log"
    log_path = get_log_file_path(log_file_name)
    with open(log_path, "w+") as outfile:
        plugin_name = find_plugin_name(command)
        if plugin_name and show_log_path:
            logger.debug(f"Writing log [{plugin_name}] to [{log_path}]")
        process = subprocess.run(command, shell=True, stderr=outfile, stdout=outfile)
    with open(log_path, "r") as outfile:
        text = outfile.read()
        remove_file(log_path)
        return text

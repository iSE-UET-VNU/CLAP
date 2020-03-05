import logging
import subprocess

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s [%(levelname)s] [%(module)s] %(message)s",
                    datefmt='%Y-%m-%d %H:%M:%S')


def get_logger(name):
    return logging.getLogger(name)


def execute_shell_command(command, extra_args=None):
    if extra_args:
        for args in extra_args:
            assert isinstance(args, dict), """Input Argument must be passed as dict={"name":"value"}"""
            arg_name = list(args.keys())[0]
            arg_val = args.get(arg_name, "")
            command += f" {arg_name} {arg_val}"
    output = subprocess.run(command, shell=True, capture_output=True)
    return output.stdout.decode("utf-8")

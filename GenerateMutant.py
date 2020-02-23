import os
import subprocess
def generateMutants(dir_path):
    os.chdir(dir_path)
    subprocess.run('java mujava.gui.GenMutantsMain')


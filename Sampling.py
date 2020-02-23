import subprocess
def sampling(model_file, k):
    subprocess.run('java -jar SPLCATool/SPLCATool.jar -t t_wise -fm ' + model_file + ' -s ' + str(k), shell=True)
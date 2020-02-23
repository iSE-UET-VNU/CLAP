import Sampling
import GenerateMutant
import GenerateConfiguration
from os import path

if __name__ == "__main__":

    Sampling.sampling("static/model.m", 2)
    Sampling.sampling("static/model.m", 3)

    feature_file = "static/feature_order.txt"

    if(path.exists("static/model.m.ca2.csv")):
        model_file_2_wise = "static/model.m.ca2.csv"
        GenerateConfiguration.generateVariants(feature_file, model_file_2_wise, 2)

    if (path.exists("static/model.m.ca2.csv")):
        model_file_3_wise = "static/model.m.ca3.csv"
        GenerateConfiguration.generateVariants(feature_file, model_file_3_wise, 3)

    #generate mutants
    GenerateMutant.generateMutants("D:\Configurable Systems\mujava_results")
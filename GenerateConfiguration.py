def readFeatureOrderFile(file_name):
    file = open(file_name)
    feature_oder = file.readlines()
    for i in range(0, len(feature_oder)):
        feature_oder[i] = feature_oder[i].replace("\n", "")
    return feature_oder

def readSamplingFile(file_name, feature_order):
    file = open(file_name, "r")
    contents = file.readlines()

    feature_seclection = []
    #sort contents according to feature_order
    for f in feature_order:
        for item in contents:
            if f in item:
                feature_seclection.append(item.replace("\n","").split(";"))
                break

    configurations = []
    for j in range(1, len(feature_seclection[0])):
        c = []
        for i in range(0, len(feature_order)):
            if feature_seclection[i][j] == 'X':
                c.append(1)
            else:
                c.append(0)
        configurations.append(c)

    return (configurations)

def writeConfigurationFile(feature_names, config, config_file_name):
    file = open(config_file_name, "w+")

    for f in feature_names:
        index = feature_names.index(f)
        if(config[index] == 1):
            file.write(f + "\n")

def generateVariants(feature_file, model_file, t_wise):
    feature_order = readFeatureOrderFile(feature_file)
    configurations = readSamplingFile( model_file, feature_order)
    print(configurations)

    print(feature_order)
    for i in range(0, len(configurations) - 1):
        config_file = "config_files/product_" + str(t_wise) + "_" + str(i) + ".config"
        writeConfigurationFile(feature_order, configurations[i], config_file)


import json

def config_setup(frames_dir, alpha, iterations, shapesPerStep, mutationsPerStep):
    with open("./config.json", "r") as jsonFile:
        config = json.load(jsonFile)

    config["input"] = f'{frames_dir}/frame*.jpg'
    config["alpha"] = alpha
    config["iterations"] = iterations
    config["candidateShapesPerStep"] = shapesPerStep
    config["shapeMutationsPerStep"] = mutationsPerStep
    config["output"] = f'{frames_dir}/jsons'

    with open("./config.json", "w") as jsonFile:
        json.dump(config, jsonFile)
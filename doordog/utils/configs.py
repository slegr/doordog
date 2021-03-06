import yaml

with open("./configs/config.yml") as f:
    configObj = yaml.load(f, Loader=yaml.FullLoader)

def get_config():
    return configObj

def get_global_config():
    return configObj['global-config']
import yaml


def read_config():
    with open("config.yaml") as f:
        config = yaml.safe_load(f)
    return config

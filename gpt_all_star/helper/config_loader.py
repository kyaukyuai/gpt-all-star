import os

import yaml


def load_configuration(file_path: str) -> dict:
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return yaml.safe_load(file)
    return {}

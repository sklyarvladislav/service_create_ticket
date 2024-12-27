import tomllib
import os

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.toml")

def load_config(file_path: str = CONFIG_PATH):
    try:
        with open(file_path, "rb") as f:
            return tomllib.load(f) 
    except Exception as e:
        raise RuntimeError(f"Error loading configuration: {e}")
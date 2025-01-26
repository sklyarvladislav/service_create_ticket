import tomllib
import os
from dotenv import load_dotenv
import json
from typing import List, Dict

load_dotenv()

CONFIG_PATH = os.getenv("CONFIG_PATH")


def load_config(file_path: str = CONFIG_PATH):
    try:
        with open(file_path, "rb") as f:
            return tomllib.load(f)
    except Exception as e:
        raise RuntimeError(f"Error loading configuration: {e}")


async def fetch_configuration() -> List[Dict]:
    with open("config.json", "r", encoding="utf-8") as file:
        data = json.load(file)

        return data["spaces"]

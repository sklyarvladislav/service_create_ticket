import os
from dynaconf import Dynaconf
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List

load_dotenv()


class SpacesConfig(BaseModel):
    spaces: List[dict]


class Config(BaseModel):
    auth_url: str
    client_id: str
    client_secret: str
    fernet_key: str
    url: str
    spaces_config: SpacesConfig


def load_config() -> Config:
    settings = Dynaconf(
        settings_files=[
            os.environ["CONFIG_PATH"],
            os.environ["SPACES_PATH"],
        ]
    )
    config = Config(
        auth_url=settings["secrets"]["auth_url"],
        client_id=settings["secrets"]["clientId"],
        client_secret=settings["secrets"]["clientSecret"],
        fernet_key=settings["secrets"]["fernet_key"],
        url=settings["settings"]["config_url"],
        spaces_config=SpacesConfig(spaces=settings["spaces"]),
    )

    return config

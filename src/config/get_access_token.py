from fastapi import HTTPException 
from cryptography.fernet import Fernet
import httpx
from src.config.get_config import load_config

config = load_config()["settings"]
decoder = Fernet(key=config["fernet_key"])
auth_url = config["auth_url"]

async def get_access_token():
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                config["auth_url"],
                data = {
                    "grant_type": "client_credentials",
                    "client_id": config["clientId"],
                    "client_secret": decoder.decrypt(config["clientSecret"].encode()).decode()
                }

            )
            response.raise_for_status() 
            return response.json()['access_token']
        except Exception as e:
            raise HTTPException(status_code=500, detail= f"error get access_token: {e}")
        
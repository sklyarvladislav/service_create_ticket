from fastapi import HTTPException
from cryptography.fernet import Fernet
import httpx

from src.infrastructure.configs import load_config

config = load_config()
decoder = Fernet(key=config.fernet_key)


async def get_access_token() -> str:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                config.auth_url,
                data={
                    "grant_type": "client_credentials",
                    "client_id": config.client_id,
                    "client_secret": decoder.decrypt(
                        config.client_secret.encode()
                    ).decode(),
                },
            )
            response.raise_for_status()
            return response.json()["access_token"]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"error get access_token: {e}")

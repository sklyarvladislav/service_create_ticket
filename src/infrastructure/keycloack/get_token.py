from cryptography.fernet import Fernet
import httpx

from src.infrastructure.configs import load_config
from src.presentation.exceptions import handle_exceptions, CustomException

config = load_config()
decoder = Fernet(key=config.fernet_key)


@handle_exceptions([httpx.RequestError, httpx.HTTPStatusError], CustomException)
async def get_access_token() -> str:
    async with httpx.AsyncClient() as client:
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

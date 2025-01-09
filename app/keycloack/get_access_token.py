import httpx
from cryptography.fernet import Fernet 

auth_url = "https://auth.bytes2b.ru/realms/Dev/protocol/openid-connect/token"
client_id = "tododdler-user-874c27f7-ff89-4167-894e-32c97e0159f4"
client_secret = "gAAAAABnf8HsAyLrhNLGvOaABQ3xtzF7c8aiLRGh4XhWQfnCKriQYzJcftxFGr3HBgtrTRTcM1UQrsrPMiTuaeACZfz0u8QGo0PUr9mmCcnhGfy-jvG6x6RkQwiQQXQ5I68G48QzCflN"
fernet_key = "PgKi9XHK7409xmwvhpzZQfuO2yekPQxtjmocjI1e6Fo="
decoder = Fernet(key=fernet_key) 


async def get_access_token():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            auth_url,
            data = {
                "grant_type": "client_credentials",
                "client_id": client_id,
                "client_secret": decoder.decrypt(client_secret.encode()).decode(),
            }
        )
        response.raise_for_status()
        access_token = response.json()['access_token']
        return access_token
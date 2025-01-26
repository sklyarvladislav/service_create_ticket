from fastapi import FastAPI
import httpx

from src.presentation.routers import router
from src.applications.client import CardCreator
from src.infrastructure.keycloack.get_token import get_access_token
from src.infrastructure.configs import load_config

config = load_config()
config_url = config.url


async def lifespan(app):
    access_token = await get_access_token()
    client = httpx.AsyncClient(
        base_url=config_url, headers={"Authorization": f"api-key {access_token}"}
    )
    app.state.card_creator = CardCreator(session=client)
    app.state.config = config
    yield

    await client.aclose()


app = FastAPI(lifespan=lifespan)

app.include_router(router)

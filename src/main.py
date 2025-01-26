import httpx
from fastapi import FastAPI
from src.routes import router
import uvicorn
from src.proccess.create_card import CardCreator
from src.config.get_access_token import get_access_token
from src.config.get_config import load_config


config_data = load_config()
config_url = config_data["settings"]["config_url"]

async def lifespan(app):
    access_token = await get_access_token()
    client = httpx.AsyncClient(
        base_url=config_url,
        headers={"Authorization": f"api-key {access_token}"}
    )
    app.state.card_creator = CardCreator(session=client)
    yield

    await client.aclose()

app = FastAPI(lifespan=lifespan)

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)

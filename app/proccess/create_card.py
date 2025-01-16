from fastapi import HTTPException
from app.schemas.schemas import CreateCard
import httpx
from app.config.get_config import load_config

config_data = load_config()
config_url = config_data["settings"]["config_url"]

async def create_card(card: CreateCard, access_token):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{config_url}/api/card",
                headers={"Authorization": f"api-key {access_token}"},
                json={
                    "board_id":card.board_id,
                    "title":card.title,
                    "description":card.description,
                    "deadline": None, 
                    "type":"bug"
                    
                }
            )
            response.raise_for_status()
            card.card_id = response.json()['id']
            
            response = await client.post(
                f"{config_url}/api/card",
                headers={"Authorization": f"api-key {access_token}"},
                json={
                    "board_id":card.board_id,
                    "title":card.title,
                    "description":card.description,
                    "deadline": None, 
                    "type":"card"
                    
                }
            )
            card_child_id = response.json()["id"]
            card.card_child_id = card_child_id

            return card.card_id
    except httpx.RequestError as e:
        raise HTTPException(status_code = 400, detail= f"failed create tododdler's card: {e}")


async def attach_files(card: CreateCard, access_token):
    try:
        async with httpx.AsyncClient() as client:
            for file in card.files:
                content = await file.read()

                response = await client.post(
                    f"{config_url}/api/card/{card.card_id}/attachment",
                    headers={"Authorization": f"api-key {access_token}"},
                    files={"file": (file.filename, content)}
                )
                response.raise_for_status() 
    except httpx.RequestError as e:
        raise HTTPException(status_code=400, detail = f"can't attach files: {e}")

async def create_card_children(card: CreateCard, access_token):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{config_url}/api/card/{card.card_id}/children",
                headers={"Authorization": f"api-key {access_token}"},
                json={"card_id":card.card_child_id}
            )
            response.raise_for_status()
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"cant create child ticket: {e}")
        
async def process_card(config, title, description, files, access_token):
    card = CreateCard(
        title=title,
        description=description,
        files=files,
        board_id=config["board_id"],
    )
    card.card_id = await create_card(card, access_token)
    await create_card_children(card, access_token)
    await attach_files(card, access_token)
    
    return card
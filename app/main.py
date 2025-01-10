from fastapi import FastAPI, Form, File, UploadFile, HTTPException
from typing import List
import uvicorn
import httpx

from config.get_config import load_config # , fetch_configuration
from config.get_access_token import get_access_token
from proccess.create_card import create_card, attach_files, create_card_children, process_card
from proccess.create_space import check_space
from schemas.schemas import CreateCard


app = FastAPI() 

config_data = load_config()
config_url = config_data["settings"]["config_url"]
@app.post("/api/tickets", summary="Create ticket")
async def create_ticket(
    title: str = Form(...),
    description: str = Form(...),
    files: List[UploadFile] = File(...)
):
    # config = await fetch_configuration(config_url)
    access_token = await get_access_token()
    spaces = await check_space(access_token, config_url)

    return spaces.json()
    
    try:
        for entry in config:
            if entry["primary"]:
                primary_ticket = await process_ticket(entry, title, description, files)
            else:
                secondary_ticket = await process_ticket(entry, title, description, files)
    except httpx.RequestError as e:
        raise HTTPException(detail=f"Internal server error: {e}")

    return {"ticket_url": f"{primary_ticket.url}/ticket/{primary_ticket.ticket_id}"}

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)

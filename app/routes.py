from fastapi import FastAPI, Form, File, UploadFile, HTTPException, APIRouter

from typing import List
import uvicorn
import httpx

from config.get_config import load_config, fetch_configuration
from config.get_access_token import get_access_token
from proccess.create_card import create_card, attach_files, create_card_children, process_card
from schemas.schemas import CreateCard

router = APIRouter()

config_data = load_config()
config_url = config_data["settings"]["config_url"]

@router.post("/api/tickets", tags=["tickets"])
async def create_ticket(
    title: str = Form(...),
    description: str = Form(...),
    files: List[UploadFile] = File(...)
):
    access_token = await get_access_token()
    config = await fetch_configuration()
    
    try:
        for entry in config:
            if entry["primary"]:
                primary_ticket = await process_card(entry, title, description, files, access_token)
            else:
                secondary_ticket = await process_card(entry, "not_primary_sklyarvlad_test", description, files, access_token)
    except httpx.RequestError as e:
        raise HTTPException(detail=f"Internal server error: {e}")

    
    return {"ticket_url": f"{config_url}/card/{primary_ticket.card_id}"}
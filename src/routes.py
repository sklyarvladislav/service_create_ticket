from fastapi import Form, File, UploadFile, Request, APIRouter

from typing import List

from src.config.get_config import load_config, fetch_configuration
from src.proccess.create_card import CardCreator
from src.schemas.schemas import CreateCard


router = APIRouter()

config_data = load_config()
config_url = config_data["settings"]["config_url"]


@router.post("/api/tickets", tags=["tickets"])
async def create_ticket(
    request: Request,
    title: str = Form(...),
    description: str = Form(...),
    files: List[UploadFile] = File(...),
):
    card_creator: CardCreator = request.app.state.card_creator
    config = await fetch_configuration()
    primary_ticket = None
    for entry in config:
        card = CreateCard(
            title=title,
            description=description,
            files=files,
            board_id=entry["board_id"],
        )
        card = await card_creator.process_card(card)

        if entry["primary"]:
            primary_ticket = card

    return {"ticket_url": f"{config_url}/card/{primary_ticket.card_id}"}

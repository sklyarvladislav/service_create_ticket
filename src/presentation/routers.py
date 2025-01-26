from fastapi import Form, File, UploadFile, Request, APIRouter

from typing import List

from src.infrastructure.configs import load_config
from src.applications.client import CardCreator
from src.entities.schemas import CreateCard


router = APIRouter()

config = load_config()
config_url = config.url


@router.post("/api/tickets", tags=["tickets"])
async def create_ticket(
    request: Request,
    title: str = Form(...),
    description: str = Form(...),
    files: List[UploadFile] = File(...),
):
    card_creator: CardCreator = request.app.state.card_creator
    config = request.app.state.config
    primary_ticket = None
    for entry in config.spaces_config.spaces:
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

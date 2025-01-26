from fastapi import UploadFile
from src.schemas.schemas import TododdlerCardCreate, CreateCard, CardType
import httpx
from src.config.get_config import load_config
from dataclasses import dataclass
from src.schemas.schemas import convert_to_tododdler
from adaptix import Retort
from typing import List

config_data = load_config()
config_url = config_data["settings"]["config_url"]

# def handle_exceptions(
#         exc: list[Exception],
#         result_exc: Exception
# ):
#     pass

retort = Retort()


@dataclass
class CardCreator:
    session: httpx.AsyncClient

    # @handle_exceptions()
    async def create_card(self, card: TododdlerCardCreate, type_card: str):
        card_data = retort.dump(card)
        card_data["type"] = type_card
        card_data["deadline"] = None

        response = await self.session.post("/api/card", json=card_data)
        response.raise_for_status()
        card.card_id = response.json()["id"]
        return card.card_id

    # @handle_exceptions()
    async def attach_files(self, card: TododdlerCardCreate, files: List[UploadFile]):
        for file in files:
            content = await file.read()
            response = await self.session.post(
                f"/api/card/{card.card_id}/attachment",
                files={"file": (file.filename, content)},
            )
            response.raise_for_status()

    # @handle_exceptions()
    async def create_card_children(
        self, parent_card: TododdlerCardCreate, child_card: TododdlerCardCreate
    ):
        response = await self.session.post(
            f"/api/card/{parent_card.card_id}/children",
            json={"card_id": child_card.card_id},
        )
        response.raise_for_status()

    async def process_card(self, card: TododdlerCardCreate) -> CreateCard:
        parent_card = convert_to_tododdler(card)
        child_card = convert_to_tododdler(card)
        parent_card.card_id = await self.create_card(parent_card, CardType.BUG.value)
        child_card.card_id = await self.create_card(child_card, CardType.CARD.value)
        await self.create_card_children(parent_card, child_card)
        await self.attach_files(parent_card, card.files)
        return parent_card

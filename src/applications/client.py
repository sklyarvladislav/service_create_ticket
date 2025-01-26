from fastapi import UploadFile
import httpx
from functools import wraps
from dataclasses import dataclass
from typing import List, Callable, Type
from adaptix import Retort

from src.entities.schemas import TododdlerCardCreate, CreateCard, convert_to_tododdler
from src.entities.constant import CardType


def handle_exceptions(exc: List[Type[Exception]], result_exc: Type[Exception] = None):
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except tuple(exc) as e:
                raise result_exc(f"An error occurred: {str(e)}") from e

        return wrapper

    return decorator


class CustomException(Exception):
    pass


retort = Retort()


@dataclass
class CardCreator:
    session: httpx.AsyncClient

    @handle_exceptions([httpx.RequestError, httpx.HTTPStatusError], CustomException)
    async def create_card(self, card: TododdlerCardCreate, type_card: str) -> int:
        card_data = retort.dump(card)
        card_data["type"] = type_card
        card_data["deadline"] = None
        response = await self.session.post("/api/card", json=card_data)
        response.raise_for_status()
        card.card_id = response.json()["id"]
        print("im create the card", type_card)
        return card.card_id

    @handle_exceptions(
        [httpx.RequestError, httpx.HTTPStatusError, ValueError, KeyError],
        CustomException,
    )
    async def attach_files(
        self, card: TododdlerCardCreate, files: List[UploadFile]
    ) -> None:
        for file in files:
            content = await file.read()
            response = await self.session.post(
                f"/api/card/{card.card_id}/attachment",
                files={"file": (file.filename, content)},
            )
        response.raise_for_status()

    @handle_exceptions([httpx.RequestError, httpx.HTTPStatusError], CustomException)
    async def create_card_children(
        self, parent_card: TododdlerCardCreate, child_card: TododdlerCardCreate
    ) -> None:
        response = await self.session.post(
            f"/api/card/{parent_card.card_id}/children",
            json={"card_id": child_card.card_id},
        )
        response.raise_for_status()

    async def process_card(self, card: TododdlerCardCreate) -> CreateCard:
        parent_card = convert_to_tododdler(card)
        child_card = convert_to_tododdler(card)
        parent_card.card_id = await self.create_card(parent_card, CardType.BUG)
        child_card.card_id = await self.create_card(child_card, CardType.CARD)
        await self.create_card_children(parent_card, child_card)
        await self.attach_files(parent_card, card.files)
        return parent_card

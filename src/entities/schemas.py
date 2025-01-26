from fastapi import UploadFile
from dataclasses import dataclass
from adaptix.conversion import get_converter
from typing import List


@dataclass
class CreateCard:
    title: str
    description: str
    files: List[UploadFile]
    board_id: int = None
    card_id: int = None
    card_child_id: int = None


@dataclass
class TododdlerCardCreate:
    board_id: int
    title: str
    description: str


convert_to_tododdler = get_converter(CreateCard, TododdlerCardCreate)

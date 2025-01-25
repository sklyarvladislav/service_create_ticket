from dataclasses import dataclass
from typing import List
from fastapi import UploadFile

@dataclass
class CreateCard():
    title: str
    description: str 
    files: List[UploadFile]
    board_id: int = None
    card_id: int = None
    card_child_id: int = None

    
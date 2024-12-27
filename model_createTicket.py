from fastapi import UploadFile 
from typing import List
from pydantic import BaseModel

class createTicket(BaseModel):
    url: str = None
    token: str = None
    title: str
    description: str 
    board_id: int = None
    files: List[UploadFile]
    ticket_id: int = None
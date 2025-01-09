from pydantic import BaseModel
from typing import List

class CreateSpace(BaseModel):
    space_id: int 

class CreateBoard(BaseModel):
    title: str 
    space_id: int 
    board_id: int

class CreateCard(BaseModel):
    url: str = None
    title: str
    description: str 
    files: List[UploadFile]
    board_id: int = None
    card_id: int = None


    

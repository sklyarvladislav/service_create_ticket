from fastapi import HTTPException, UploadFile
from pydantic import BaseModel
from typing import List
import httpx

class createTicket(BaseModel):
    url: str = None
    token: str = None
    title: str
    description: str 
    board_id: int = None
    files: List[UploadFile]
    ticket_id: int = None

async def create_kaiten_ticket(ticket: createTicket):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{ticket.url}/api/latest/cards",
                headers={"Authorization": f"Bearer {ticket.token}"},
                json={
                    "title":ticket.title,
                    "description":ticket.description,
                    "board_id":ticket.board_id 
                }
            )
            response.raise_for_status()
            ticket_id = response.json()["id"]

            return ticket_id
    except httpx.RequestError as e:
        raise HTTPException(status_code = 400, detail= f"can't create kaiten ticket: {e}")

async def attach_files(ticket: createTicket):
    try:
        async with httpx.AsyncClient() as client:
            for file in ticket.files:
                content = await file.read()

                response = await client.post(
                    f"{ticket.url}/api/latest/cards/{ticket.ticket_id}/files",
                    headers={"Authorization": f"Bearer {ticket.token}"},
                    files={"file": (file.filename, content)}
                )
                response.raise_for_status() 
    except httpx.RequestError as e:
        raise HTTPException(status_code=400, detail = f"can't attach files: {e}")

async def create_kaiten_child_ticket(ticket: createTicket):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{ticket.url}/api/latest/cards/{ticket.ticket_id}/children",
                headers={"Authorization": f"Bearer {ticket.token}"},
            )
            response.raise_for_status()
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"cant create child ticket: {e}")
        
async def process_ticket(config, title, description, files):
    ticket = createTicket(
        url=config["url"],
        token=config["token"],
        title=title,
        description=description,
        files=files,
        board_id=config["board_id"]
    )
    ticket.ticket_id = await create_kaiten_ticket(ticket)
    await attach_files(ticket)
    await create_kaiten_child_ticket(ticket)
    return ticket

from fastapi import HTTPException, UploadFile
from schemas.schemas import CreateCard
import httpx

async def create_card(ticket: CreateCard):
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

async def attach_files(ticket: CreateCard):
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

async def create_card_children(ticket: CreateCard):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{ticket.url}/api/latest/cards/{ticket.ticket_id}/children",
                headers={"Authorization": f"Bearer {ticket.token}"},
            )
            response.raise_for_status()
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"cant create child ticket: {e}")
        
async def process_card(config, title, description, files):
    card = CreateCard(
        url=config["url"],
        token=config["token"],
        title=title,
        description=description,
        files=files,
        board_id=config["board_id"]
    )
    ticket.ticket_id = await create_card(card)
    await attach_files(card)
    await create_card_children(card)
    return card

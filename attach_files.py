from fastapi import HTTPException 
from model_createTicket import createTicket 
import httpx 
import asyncio

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

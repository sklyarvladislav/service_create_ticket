from fastapi import HTTPException
from model_createTicket import createTicket
import asyncio 
import httpx



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
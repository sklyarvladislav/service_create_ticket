from model_createTicket import createTicket 
import httpx
import asyncio 

async def create_kaiten_child_ticket(ticket: createTicket):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{ticket.url}/api/latest/cards/{ticket.ticket_id}/children",
            headers={"Authorization": f"Bearer {ticket.token}"},
            json={
                "parent_id":ticket.ticket_id,
            }
        )
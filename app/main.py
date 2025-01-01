from fastapi import FastAPI, Form, File, UploadFile, HTTPException
from typing import List
import uvicorn
import httpx

from config.get_config import load_config
from config.fetch_configuration import fetch_configuration
from kaiten_tickets.create_ticket import createTicket, create_kaiten_ticket, attach_files, create_kaiten_child_ticket, process_ticket

app = FastAPI() #add comment

config_data = load_config()
config_url = config_data["settings"]["config_url"]

@app.post("/api/tickets", summary="Create ticket")
async def create_ticket(
    title: str = Form(...),
    description: str = Form(...),
    files: List[UploadFile] = File(...)
):
    config = await fetch_configuration(config_url)

    try:
        for entry in config:
            if entry["primary"]:
                primary_ticket = await process_ticket(entry, title, description, files)
            else:
                secondary_ticket = await process_ticket(entry, title, description, files)
    except httpx.RequestError as e:
        raise HTTPException(detail=f"Internal server error: {e}")

    return {"ticket_url": f"{primary_ticket.url}/ticket/{primary_ticket.ticket_id}"}

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)

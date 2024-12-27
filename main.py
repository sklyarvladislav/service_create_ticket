from fastapi import FastAPI, Form, File, UploadFile, HTTPException
from typing import List 
import uvicorn
from pydantic import BaseModel
import httpx
import asyncio 
import json
import os 
from get_config import load_config
from model_createTicket import createTicket
from fetch_configuration import fetch_configuration
from create_kaiten_ticket import create_kaiten_ticket
from attach_files import attach_files
from create_kaiten_child_ticket import create_kaiten_child_ticket


app = FastAPI()

config_data = load_config()
config_url = config_data["settings"]["config_url"]



@app.post("/api/tickets", summary = "create ticket")
async def create_ticket(
    title: str = Form(...),
    description: str = Form(...),
    files: List[UploadFile] = File(...)
):

    config = await fetch_configuration(config_url)

    try:
        for primary in range(len(config)): 
            if config[primary]["primary"]:
                ticket = createTicket(
                    url=config[primary]["url"],
                    token=config[primary]["token"],
                    title=title,
                    description=description,
                    files=files,
                    board_id=config[primary]["board_id"],
                ) 

            ticket.ticket_id = await create_kaiten_ticket(ticket)
            await attach_files(ticket)
            await create_kaiten_child_ticket(ticket)
        else:
            ticket_not_primary = createTicket(
                url=config[primary]["url"],
                token=config[primary]["token"],
                title=title,
                description=description,
                files=files,
                board_id=config[primary]["board_id"]
            )

            ticket_not_primary.ticket_id = await create_kaiten_ticket(ticket_not_primary)
            await attach_files(ticket_not_primary)
            await create_kaiten_child_ticket(ticket_not_primary)
    except httpx.RequestError as e:
            raise HTTPException(detail = e)

    return {"ticket_url": f"{ticket.url}/ticket/{ticket.ticket_id}"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload = True)
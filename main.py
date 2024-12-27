from fastapi import FastAPI, Form, File, UploadFile, HTTPException
from typing import List 
import uvicorn
from pydantic import BaseModel
import httpx
import asyncio 
import json
import os 
import tomllib


app = FastAPI()

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.toml")

def load_config(file_path: str = CONFIG_PATH):
    try:
        with open(file_path, "rb") as f:
            return tomllib.load(f) 
    except Exception as e:
        raise RuntimeError(f"Error loading configuration: {e}")

config_data = load_config()
config_url = config_data["settings"]["config_url"]


class createTicket(BaseModel):
    url: str = None
    token: str = None
    title: str
    description: str 
    board_id: int = None
    files: List[UploadFile]
    ticket_id: int = None

async def fetch_configuration(url: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url) 
            response.raise_for_status()
            data = response.json()
            return data["kaiten_urls"] 
    except httpx.RequestError as e:
        raise HTTPException(status_code = 500, detail = f"Internal server error: {e}")

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
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{ticket.url}/api/latest/cards/{ticket.ticket_id}/children",
            headers={"Authorization": f"Bearer {ticket.token}"},
            json={
                "parent_id":ticket.ticket_id,
            }
        )

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
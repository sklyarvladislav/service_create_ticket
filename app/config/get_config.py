import tomllib
import os
from dotenv import load_dotenv
from fastapi import HTTPException
import httpx

load_dotenv() 

CONFIG_PATH = os.getenv('CONFIG_PATH') 

def load_config(file_path: str = CONFIG_PATH):
    try:
        with open(file_path, "rb") as f:
            return tomllib.load(f) 
    except Exception as e:
        raise RuntimeError(f"Error loading configuration: {e}")

async def fetch_configuration(url: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url) 
            response.raise_for_status()
            data = response.json()
            return data["kaiten_urls"] 
    except httpx.RequestError as e:
        raise HTTPException(status_code = 500, detail = f"Internal server error: {e}")

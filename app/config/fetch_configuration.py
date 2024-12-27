from fastapi import HTTPException
import httpx
import asyncio 

async def fetch_configuration(url: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url) 
            response.raise_for_status()
            data = response.json()
            return data["kaiten_urls"] 
    except httpx.RequestError as e:
        raise HTTPException(status_code = 500, detail = f"Internal server error: {e}")

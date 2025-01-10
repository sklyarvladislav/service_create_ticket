from fastapi import HTTPException
import httpx 

async def check_space(
    access_token: str, 
    config_url: str,
):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{config_url}/api/space",
                headers={
                    "Content-type": "application/json", 
                    "Authorization": f"Bearer {access_token}"
                }
            )
            response.raise_for_status()
            return response.json()
    except httpx.RequestError as e:
        raise HTTPException(status_code=400, detail="bad request")


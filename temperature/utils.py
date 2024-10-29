import os

import httpx
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from dotenv import load_dotenv

from weather.crud import get_all_cities
from dependencies import get_db

load_dotenv()

API_URL = os.getenv("API_URL")
API_KEY = os.getenv("API_KEY")


async def check_service_connection():
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{API_URL}/current.json", params={"key": API_KEY, "q": "London"}
        )
    if response.status_code != 200:
        error_detail = response.json() if response.headers.get("Content-Type") == "application/json" else response.text
        raise HTTPException(status_code=response.status_code, detail=error_detail)
    else:
        return True


async def get_temperature(db: AsyncSession = Depends(get_db)):
    city_list = await get_all_cities(db)
    response = {}
    async with httpx.AsyncClient() as client:
        for city in city_list:
            result = await client.get(
                f"{API_URL}/current.json", params={"key": API_KEY, "q": city.name}
            )
            response[city.name] = result.json()
            response[city.name]["city_id"] = city.id
    return response

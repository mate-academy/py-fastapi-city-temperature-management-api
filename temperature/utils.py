import httpx
import os
from typing import Optional
from fastapi import HTTPException
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")


async def fetch_city_temperature(city_name: str) -> Optional[float]:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}?q={city_name}&appid={API_KEY}&units=metric"
        )
        data = response.json()
        if response.status_code == 200:
            return data["main"]["temp"]
        raise HTTPException(status_code=404, detail="City not found")

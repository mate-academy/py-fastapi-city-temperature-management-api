import os

import httpx
from fastapi import HTTPException

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
URL = "http://api.weatherapi.com/v1/current.json"


async def fetch_temperature_data(city_name: str) -> float:
    params = {"key": API_KEY, "q": city_name}
    async with httpx.AsyncClient() as client:
        response = await client.get(URL, params=params)

        if response.status_code != 200:
            raise HTTPException(
                status_code=400, detail="Failed to fetch temperature data"
            )

    response_data = response.json()
    current_weather = response_data["current"]
    temp_c = current_weather["temp_c"]
    return temp_c

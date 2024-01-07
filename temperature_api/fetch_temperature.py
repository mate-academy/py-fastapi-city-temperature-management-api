import os

import httpx
from fastapi import HTTPException


API_URL = "https://api.openweathermap.org/data/2.5/weather"
API_KEY = os.getenv("API_KEY")


async def fetch_temperature_for_city(city_name: str) -> float:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            API_URL,
            params={"appid": API_KEY, "q": city_name, "units": "metric"},
        )

        if response.status_code == 200:
            weather_data = response.json()
            temperature = weather_data["main"]["temp"]
            return temperature
        else:
            raise HTTPException(
                status_code=response.status_code,
                detail="Failed to fetch temperature data",
            )

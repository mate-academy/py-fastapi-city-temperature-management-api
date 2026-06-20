from datetime import datetime
import os

import httpx
from dotenv import load_dotenv

load_dotenv()


BASE_URL = "https://api.weatherapi.com/v1/current.json"


async def fetch_temperature(city_name: str) -> dict:
    api_key = os.getenv("WEATHER_API_KEY")

    async with httpx.AsyncClient() as client:
        response = await client.get(
            BASE_URL,
            params={
                "key": api_key,
                "q": city_name,
            },
        )

    response.raise_for_status()
    data = response.json()

    return {
        "temperature": data["current"]["temp_c"],
        "date_time": datetime.strptime(
            data["current"]["last_updated"],
            "%Y-%m-%d %H:%M",
        ),
    }

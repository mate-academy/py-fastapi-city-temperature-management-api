import os
import httpx
from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv("WEATHER_API_KEY")

if API_KEY is None:
    raise RuntimeError("WEATHER_API_KEY is missing")


async def get_current_temperature(city_name: str) -> float:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.weatherapi.com/v1/current.json",
            params={
                "key": API_KEY,
                "q": city_name,
            }
        )
    response.raise_for_status()

    data = response.json()
    temperature = data["current"]["temp_c"]

    return temperature


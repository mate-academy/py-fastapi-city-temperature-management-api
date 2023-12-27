import os
import httpx

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ["API_KEY"]
URL = "https://api.weatherapi.com/v1/current.json"


async def get_temperature(city) -> dict:
    async with httpx.AsyncClient() as client:
        params = {"key": API_KEY, "q": city.name}
        response = await client.get(URL, params=params, timeout=5)

        return response.json()

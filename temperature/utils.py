import json
import os

import httpx
from dotenv import load_dotenv

load_dotenv()

URL = "https://api.weatherapi.com/v1/current.json?"
API_KEY = os.environ.get("API_KEY")


async def fetch_temperature(city_name: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            URL,
            params={"key": API_KEY, "q": city_name}
        )
        data = json.loads(response.content)
        return data['current']['temp_c']

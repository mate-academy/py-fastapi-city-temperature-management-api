import os
import httpx
from dotenv import load_dotenv


load_dotenv()

API_KEY = os.environ.get("API_KEY")
URL = "https://api.weatherapi.com/v1/current.json?"


async def get_temperature_from_weatherapi(city_name: str) -> int:
    async with httpx.AsyncClient() as client:
        response = await client.get(URL + f"q={city_name}&key={API_KEY}")
        response.raise_for_status()  # Raises an error for non-200 responses
        data = response.json()
        return int(data["current"]["temp_c"])

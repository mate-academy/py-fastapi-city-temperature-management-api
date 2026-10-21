import httpx
from dotenv import load_dotenv

from settings import settings

load_dotenv()

API_KEY = settings.API_KEY
WEATHER_URL = "https://api.weatherapi.com/v1/current.json"


async def get_weather(city: str) -> float:
    if not API_KEY:
        raise httpx.HTTPStatusError("API key not provided")
    async with httpx.AsyncClient() as client:
        response = await client.get(WEATHER_URL + f"?q={city}&key=" + API_KEY)
        if response.status_code == 200:
            data = response.json()
            return data["current"]["temp_c"]
        raise httpx.HTTPStatusError("Error getting weather data")

import httpx
from dotenv import load_dotenv
from fastapi import HTTPException
from starlette import status

from settings import settings

load_dotenv()

API_KEY = settings.API_KEY
WEATHER_URL = "https://api.weatherapi.com/v1/current.json"


async def get_weather(city: str) -> float:
    if not API_KEY:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="API key not provided",
        )
    async with httpx.AsyncClient() as client:
        response = await client.get(WEATHER_URL + f"?q={city}&key=" + API_KEY)
        if response.status_code == 200:
            data = response.json()
            return data["current"]["temp_c"]
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error getting weather data",
        )

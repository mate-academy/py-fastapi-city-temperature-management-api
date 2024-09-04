import os
import httpx
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("API_KEY")


async def get_city_temperature(city_name: str):
    async with httpx.AsyncClient() as client:
        res = await client.get(f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city_name}&aqi=no")
        return res.json()["current"]["temp_c"]

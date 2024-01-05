import os
import httpx

from dotenv import load_dotenv

load_dotenv()

URL = "http://api.weatherapi.com/v1/current.json"
API_KEY = os.environ.get("WEATHER_API_KEY")


async def get_temperature(city: str, client: httpx.AsyncClient) -> float:
    params = {"key": API_KEY, "q": city, "aqi": "no"}
    response = await client.get(URL, params=params)
    data = response.json()
    return data['current']['temp_c']

import os

import httpx
from dotenv import load_dotenv
from fastapi import HTTPException
from datetime import datetime, UTC

load_dotenv()

WEATHER_API = os.getenv("WEATHER_API")
API_KEY = os.getenv("API_KEY")


async def fetch_temperature(city_name: str, city_id: int):
    client = httpx.AsyncClient()
    url = WEATHER_API.format(city=city_name.replace(" ", "+"), API_KEY=API_KEY)
    try:
        res = await client.get(url)
    except httpx.RequestError:
        raise HTTPException(
            detail="Network error while fetching weather data", status_code=404
        )
    if res.status_code != 200:
        raise HTTPException(
            status_code=res.status_code,
        )
    data = res.json()
    date = datetime.fromtimestamp(data.get("dt"), UTC)
    return {
        "city_id": city_id,
        "temperature": data["main"]["temp"],
        "date_time": date,
    }

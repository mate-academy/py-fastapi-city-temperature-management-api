import os

import httpx
from dotenv import load_dotenv
from fastapi import HTTPException
from datetime import datetime, UTC

load_dotenv()

WEATHER_API = os.getenv("WEATHER_API")
API_KEY = os.getenv("API_KEY")

if not WEATHER_API or not API_KEY:
    raise RuntimeError(
        "Configuration error: WEATHER_API or API_KEY not set in environment."
    )


async def fetch_temperature(city_name: str, city_id: int):
    async with httpx.AsyncClient() as client:
        url = WEATHER_API.format(city=city_name.replace(" ", "+"), API_KEY=API_KEY)
        try:
            res = await client.get(url, timeout=5)
        except httpx.ConnectTimeout:
            raise HTTPException(
                status_code=504,
                detail="Connection to weather API timed out",
            )
        except httpx.RequestError:
            raise HTTPException(
                detail="Network error while fetching weather data", status_code=404
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Unexpected error fetching weather data: {e}",
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

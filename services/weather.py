import os

import httpx
from fastapi import HTTPException

API_KEY = os.getenv("API_KEY")


async def fetch_temperature(city_name: str) -> float:
    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": city_name,
        "appid": API_KEY,
        "units": "metric",
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params)
            response.raise_for_status()
        except httpx.HTTPError:
            raise HTTPException(
                status_code=502,
                detail="The server couldn't fulfill the request.",
            )

    data = response.json()
    main = data.get("main")
    if not main or "temp" not in main:
        raise HTTPException(
            status_code=502,
            detail="The server couldn't fulfill the request.",
        )

    return main["temp"]

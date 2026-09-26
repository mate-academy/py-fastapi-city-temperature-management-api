from urllib.parse import quote

import httpx


WEATHER_URL = "https://wttr.in/{city}"

async def fetch_temperature(city_name: str) -> float:
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(
            WEATHER_URL.format(city=quote(city_name)),
            params={"format": "j1"},
        )
        response.raise_for_status()
        data = response.json()
        return float(data["current_condition"][0]["temp_C"])
import os
import httpx


async def get_temp(city: str) -> float | None:
    url = f"http://api.weatherapi.com/v1/current.json?key={os.getenv('API_KEY')}&q={city}"

    try:
        async with httpx.AsyncClient() as client:
            res = await client.get(url)
            return res.json()["current"]["temp_c"]
    except Exception:
        return None

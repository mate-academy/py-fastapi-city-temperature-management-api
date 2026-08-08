import os
import httpx
from dotenv import load_dotenv
load_dotenv()


async def get_temp(city: str):
    base_url = os.environ["BASE_WEATHER_API_URL"]
    api_key = os.environ["WEATHER_API_KEY"]

    params = {
        "access_key": api_key,
        "query": city,
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(base_url, params=params)

    response.raise_for_status()

    data = response.json()

    if "current" not in data:
        raise ValueError(
            f"Weather API returned an error: {data}"
        )

    return float(data["current"]["temperature"])

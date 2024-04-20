from fastapi import HTTPException
from httpx import AsyncClient
import os
from dotenv import load_dotenv


load_dotenv()

URL = os.environ.get("WEATHER_API_URL")
API_KEY = os.environ.get("API_KEY")


async def get_temperatures(city_name: str, client: AsyncClient) -> str:

    print(f"Performing request to Weather API for city {city_name}...")
    response = await client.get(
        url=URL,
        params={
            "key": API_KEY,
            "q": city_name
        }
    )

    if response.status_code >= 400:
        print(f"Request failed with status code {response.status_code}\n"
              f"{response.text}")

        raise HTTPException(
            status_code=response.status_code, detail=response.text
        )

    json_format = response.json()
    temperature = json_format["current"]["temp_c"]

    return temperature

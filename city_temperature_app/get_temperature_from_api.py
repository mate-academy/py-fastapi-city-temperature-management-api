import os
from datetime import datetime
from typing import Callable

import httpx
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession

from city_temperature_app import (
    crud,
    models,
    schemas,
)

load_dotenv()


def get_env_variables() -> tuple[str, str]:
    weather_api_key = os.getenv("WEATHER_API_KEY")
    weather_api_url = os.getenv("WEATHER_API_URL")

    if not weather_api_key:
        raise ValueError("WEATHER_API_KEY not found (check your .env file)")
    if not weather_api_url:
        raise ValueError("WEATHER_API_URL not found (check your .env file)")

    return weather_api_key, weather_api_url


async def fetch_temperatures_from_api(
        client: httpx.AsyncClient,
        city: models.City,
        db_session_factory: Callable[[], AsyncSession],
) -> None:
    api_key, api_url = get_env_variables()
    try:
        response = await client.get(
            api_url, params={"key": api_key, "q": city.name}
        )
        response.raise_for_status()
    except httpx.HTTPStatusError as http_err:
        print(f"HTTP error occurred: {http_err} - for city: {city.name}")
        return

    try:
        data = response.json()
        temperature = schemas.TemperatureCreate(
            city_id=city.id,
            date_time=datetime.now().strftime("%Y-%m-%d %H:%M"),
            temperature=data["current"]["temp_c"],
        )
    except (KeyError, ValueError) as json_err:
        print(f"JSON parsing error: {json_err} - for city: {city.name}")
        return

    try:
        async with db_session_factory() as new_db_session:
            await crud.create_temperature(new_db_session, temperature)
    except Exception as db_err:
        print(f"Database error: {db_err} - "
              f"while saving temperature for city: {city.name}")

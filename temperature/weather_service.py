from datetime import datetime

import httpx
from sqlalchemy.ext.asyncio import AsyncSession

from city import crud as city_crud
from temperature import crud
from temperature.models import Temperature

GEOCODING_URL = (
    "https://geocoding-api.open-meteo.com/v1/search"
)
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"


async def get_temperature_for_city(
    client: httpx.AsyncClient, city_name: str
) -> float | None:
    try:
        geo_response = await client.get(
            GEOCODING_URL,
            params={"name": city_name, "count": 1},
        )
        geo_response.raise_for_status()
        geo_data = geo_response.json()

        if "results" not in geo_data:
            return None

        location = geo_data["results"][0]
        lat = location["latitude"]
        lon = location["longitude"]

        weather_response = await client.get(
            WEATHER_URL,
            params={
                "latitude": lat,
                "longitude": lon,
                "current_weather": True,
            },
        )
        weather_response.raise_for_status()
        weather_data = weather_response.json()

        return weather_data["current_weather"]["temperature"]
    except (httpx.HTTPStatusError, httpx.RequestError, KeyError):
        return None


async def update_all_temperatures(
    db: AsyncSession,
    client: httpx.AsyncClient,
) -> list[Temperature]:
    cities = await city_crud.get_cities(db)
    results = []

    for city in cities:
        temperature = await get_temperature_for_city(
            client, city.name
        )
        if temperature is not None:
            temp_record = await crud.create_temperature(
                db=db,
                city_id=city.id,
                temperature=temperature,
                date_time=datetime.now(),
            )
            results.append(temp_record)

    return results

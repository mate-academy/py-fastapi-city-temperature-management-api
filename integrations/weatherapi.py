import asyncio
import os
import httpx

from dotenv import load_dotenv

from city.models import City
from temperature.schemas import TemperatureCreate

load_dotenv()

API_KEY = os.getenv("WEATHER_API_KEY")
BASE_URL = "http://api.weatherapi.com/v1/current.json?"


async def get_temperature_value(
    city: City,
    client: httpx.AsyncClient,
    semaphore: asyncio.Semaphore,
) -> TemperatureCreate:
    if not API_KEY:
        raise RuntimeError("API key for weatherapi not found")

    try:
        async with semaphore:
            response = await client.get(
                BASE_URL,
                params={
                    "key": API_KEY,
                    "q": city.name,
                },
            )
            response.raise_for_status()
            res = response.json()

        return TemperatureCreate(
            city_id=city.id,
            temperature=res["current"]["temp_c"],
            date_time=res["current"]["last_updated"],
        )
    except httpx.HTTPError as exc:
        raise RuntimeError(
            f"Can't get weather for city with name '{city.name}'"
        ) from exc


async def get_temperatures_for_cities(
    cities: list[City],
    concurrency_limit: int = 10,
) -> tuple[list[TemperatureCreate], list[str]]:
    if concurrency_limit < 1:
        raise ValueError("concurrency_limit must be >= 1")
    if not API_KEY:
        raise RuntimeError("API key for weatherapi not found")

    if not cities:
        return [], []

    semaphore = asyncio.Semaphore(concurrency_limit)

    async with httpx.AsyncClient(timeout=10.0) as client:
        tasks = [
            get_temperature_value(city=city, client=client, semaphore=semaphore)
            for city in cities
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)

    temperatures: list[TemperatureCreate] = []
    errors: list[str] = []

    for city, result in zip(cities, results):
        if isinstance(result, Exception):
            errors.append(f"{city.name}: {result}")
            continue
        temperatures.append(result)

    return temperatures, errors

import os
from typing import List
import httpx

from dotenv import load_dotenv

import models
import utils


load_dotenv(override=True)


async def read_temperature_api(cities: List[models.City]) -> dict[int, float]:
    OPEN_WEATHER_URL = os.getenv("OPEN_WEATHER_URL")
    OPEN_WEATHER_API_KEY = os.getenv("OPEN_WEATHER_API_KEY")

    if not OPEN_WEATHER_URL or not OPEN_WEATHER_API_KEY:
        raise ValueError(
            (
                "Environment variables OPEN_WEATHER_URL and "
                "OPEN_WEATHER_API_KEY must be set."
            )
        )

    temperatures = {}

    async with httpx.AsyncClient(timeout=10.0) as client:
        for city in cities:
            try:
                resp = await client.get(
                    url=OPEN_WEATHER_URL,
                    params={
                        "q": city.name,
                        "appid": OPEN_WEATHER_API_KEY,
                        "units": "metric"
                    }
                )
                resp.raise_for_status()

                data = resp.json()
                if "main" not in data or "temp" not in data["main"]:
                    utils.logger.error(
                        f"Unexpected response format for city "
                        f"'{city.name}': {data}"
                    )
                    continue

                city_temperature = data["main"]["temp"]
                temperatures[city.id] = city_temperature
            except (
                httpx.HTTPError,
                httpx.TimeoutException,
                httpx.ConnectError,
                httpx.ReadError
            ) as exc:
                utils.logger.error(
                    f"Error fetching data for city '{city.name}' "
                    f"(ID: {city.id}): {exc}"
                )
                continue


    return temperatures

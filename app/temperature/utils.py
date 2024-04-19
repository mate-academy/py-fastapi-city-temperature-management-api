import asyncio
import os
from datetime import datetime

import httpx
from dotenv import load_dotenv
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.city.models import City
from app.temperature.models import Temperature

load_dotenv()

URL = "http://api.weatherapi.com/v1/current.json"
API_KEY = os.getenv("API_KEY")


class WeatherService:

    @classmethod
    async def _get_response_by_city(
        cls,
        client: httpx.AsyncClient,
        city: str,
        url: str = URL,
    ) -> httpx.Response:
        return await client.get(url=url, params={"key": API_KEY, "q": city})

    @classmethod
    async def _create_task_group(cls, client: httpx, cities: list) -> list:
        async with asyncio.TaskGroup() as tg:
            tasks = [
                tg.create_task(cls._get_response_by_city(client=client, city=city))
                for city in cities
            ]

        return tasks

    @classmethod
    async def get_all_cities_weather(cls, cities: list) -> dict:
        async with httpx.AsyncClient() as client:
            tasks = await cls._create_task_group(client=client, cities=cities)

            weather = {}

            for city, task in zip(cities, tasks):
                try:
                    result = await task
                    result.raise_for_status()
                    temperature = result.json().get("current").get("temp_c")
                    weather[city] = temperature
                except Exception as e:
                    raise HTTPException(status_code=400, detail=str(e))

        return weather


def create_temperature_instance(
    db: AsyncSession,
    city: City,
    weather_data: float,
) -> None:
    temperature_instance = Temperature(
        city_id=city.id,
        temperature=weather_data,
        date_time=datetime.now(),
    )
    db.add(temperature_instance)


def update_temperature_instance(
    temperature_instance: Temperature,
    weather_data: float
) -> None:
    temperature_instance.temperature = weather_data
    temperature_instance.date_time = datetime.now()

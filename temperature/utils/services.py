import asyncio
import os

import httpx
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()


class WeatherService:
    URL = "http://api.weatherapi.com/v1/current.json"
    API_KEY = os.getenv("WEATHER_API_KEY")

    @classmethod
    async def _get_response_by_city(
        cls, client: httpx.AsyncClient, city: str, url: str = URL
    ) -> httpx.Response:
        res = await client.get(url=url, params={"key": cls.API_KEY, "q": city})

        return res

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
                    res = await task
                    res.raise_for_status()
                    temperature = res.json().get("current").get("temp_c")
                    weather[city] = temperature
                except Exception as e:
                    raise HTTPException(status_code=400, detail=str(e))

        return weather

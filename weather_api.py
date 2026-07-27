from dependencies import OPENWEATHER_API_KEY
from sqlalchemy.orm import Session
from city_api import city_models
from datetime import timezone
from temperature_api import temp_crud

import httpx
import asyncio
import datetime


async def get_weather_for_city(
        city_name: str
    ):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={
                "q": city_name,
                "appid": OPENWEATHER_API_KEY,
                "units": "metric"
            }
            ) 
        return response.json()


async def create_temperature_from_list(
        db: Session,
        city_list: list[city_models.DBCity]
):
    weather_for_city_list = [get_weather_for_city(city.name) for city in city_list]
    weather_values = await asyncio.gather(*weather_for_city_list, return_exceptions=True)

    for index, values in enumerate(weather_values):
        if isinstance(values, Exception) or values.get("cod") != 200:
            continue
        else:
            temp_crud.create_temperature(
                db=db,
                city_id=city_list[index].id,
                date_time=datetime.datetime.fromtimestamp(values["dt"], tz=timezone.utc),
                temperature=values["main"]["temp"]
                )

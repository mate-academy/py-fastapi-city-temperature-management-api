import asyncio
import httpx
from sqlalchemy.orm import Session

from city.models import CityDB
from temperature.models import TemperatureDB
from settings import settings


URL_WEATHER = "https://api.openweathermap.org/data/2.5/weather"


async def get_temperature_by_city(city: str):
    url = f"{URL_WEATHER}?q={city}&appid={settings.WEATHER_API}&units=metric"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        temp = response.json()["main"]["temp"]
    return temp


def get_temperature_sync(city: str):
    return asyncio.run(get_temperature_by_city(city))


def temperature_update(db: Session):
    cities = db.query(CityDB).all()
    for city in cities:
        temperature = get_temperature_sync(city.name)
        db_temp = TemperatureDB(
            city_id=city.id,
            temperature=temperature
        )
        db.add(db_temp)
        db.commit()
    return "{New weather has been created for cities that are in the database}"


def get_temperatures(city_id: int | None, db: Session):
    queryset = db.query(TemperatureDB)

    if city_id is not None:
        queryset = queryset.filter(TemperatureDB.city_id == city_id)

    return queryset.all()

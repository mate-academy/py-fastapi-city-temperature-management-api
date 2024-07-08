import asyncio
from datetime import datetime
import os

import requests
from sqlalchemy.orm import Session

from city.crud import get_cities_list
from city.models import DBCity
from temperature.models import DBTemperature


def get_temperatures(db: Session, city_id: int | None = None) -> list[DBTemperature]:
    queryset = db.query(DBTemperature)

    if city_id is not None:
        queryset = queryset.filter(DBTemperature.city_id == city_id)

    return queryset.all()


async def get_lastest_temperature_from_external_api(city_name: str) -> tuple[float, datetime]:
    api_key = os.getenv("WEATHER_API_KEY")

    if api_key is None:
        raise ValueError("API_KEY environment variable is not set")

    url = "http://api.weatherapi.com/v1/current.json"
    payload = {"key": api_key, "q": city_name}
    result = await asyncio.to_thread(requests.get, url, params=payload)
    data = result.json()
    temperature = data["current"]["temp_c"]
    date_time = datetime.strptime(data["current"]["last_updated"], "%Y-%m-%d %H:%M")

    return temperature, date_time


async def create_city_temperature(db: Session, db_city: DBCity) -> DBTemperature:
    temperature, date_time = await get_lastest_temperature_from_external_api(db_city.name)
    db_temperature = DBTemperature(
        city_id=db_city.id,
        temperature=temperature,
        date_time=date_time,
    )
    db.add(db_temperature)
    db.commit()
    db.refresh(db_temperature)
    return db_temperature


async def update_city_temperature(db: Session, db_temperature: DBTemperature) -> DBTemperature:
    temperature, date_time = await get_lastest_temperature_from_external_api(db_temperature.city.name)
    db_temperature.temperature = temperature
    db_temperature.date_time = date_time
    db.commit()
    db.refresh(db_temperature)
    return db_temperature


async def update_all_temperatures(db: Session) -> None:
    db_cities = get_cities_list(db=db)
    for db_city in db_cities:
        if db_city.temperature:
            await update_city_temperature(db=db, db_temperature=db_city.temperature)
        else:
            await create_city_temperature(db=db, db_city=db_city)

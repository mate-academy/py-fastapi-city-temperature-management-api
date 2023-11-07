import asyncio
import os
from datetime import datetime

import httpx
from dotenv import load_dotenv
from fastapi import HTTPException
from httpx import HTTPError
from sqlalchemy.orm import Session

from city.models import City
from . import models
from city.crud import get_all_cities


load_dotenv()


URL = "http://api.weatherapi.com/v1/current.json"
WEATHER_URL = f"{URL}?key={os.environ.get('WEATHER_API_KEY')}"


def get_all_temperatures(db: Session):
    return db.query(models.Temperature).all()


def get_temperature_by_city_id(db: Session, city_id: int):
    db_temperature = db.query(models.Temperature).filter(
        models.Temperature.city_id == city_id
    ).first()

    if db_temperature is None:
        raise HTTPException(status_code=404, detail="City not found")

    return db_temperature


def change_temperature_status(
        db: Session,
        city_id: int,
        date_time: str,
        temperature: int
):
    try:
        weather = get_temperature_by_city_id(db=db, city_id=city_id)
    except HTTPException:
        db_weather = models.Temperature(
            city_id=city_id,
            date_time=datetime.strptime(date_time, "%Y-%m-%d %H:%M"),
            temperature=temperature
        )
        db.add(db_weather)
        db.commit()
        db.refresh(db_weather)
    else:
        weather.date_time = datetime.strptime(date_time, "%Y-%m-%d %H:%M")
        weather.temperature = temperature
        db.commit()


async def update_weather_data(db: Session, url: str, city: City, client: httpx.AsyncClient):

    try:
        weather = await client.get(url=f"{url}&q={city.name}")
        current_weather = weather.json()["current"]

        date_time = current_weather["last_updated"]
        temperature = current_weather["temp_c"]

        change_temperature_status(
            db=db,
            city_id=city.id,
            date_time=date_time,
            temperature=temperature
        )
    except HTTPError as http_exception:
        print(str(http_exception))
    except Exception as exception:
        print(str(exception))


async def update_temperatures(db: Session):
    cities = get_all_cities(db)

    async with httpx.AsyncClient() as client:
        async with asyncio.TaskGroup() as tg:
            [
                tg.create_task(
                    update_weather_data(db=db, url=WEATHER_URL, city=city, client=client)
                )
                for city in cities
            ]

import asyncio
from datetime import datetime

import httpx
from fastapi import HTTPException
from sqlalchemy import update
from sqlalchemy.orm import Session

from src.city.models import DBCity
from .models import DBTemperature

api_key = "4c138910c9bd1151ed4fa64d9f91afc8"

base_url = f"http://api.openweathermap.org/data/2.5/weather?appid={api_key}&q="


async def get_city_current_temperature(city_name: str) -> int | None:
    async with httpx.AsyncClient() as client:
        response = await client.get(base_url + city_name)
        weather = response.json()

    if weather["cod"] not in [401, 404, 429, 500, 502, 503, 504]:
        celsius_temp = weather["main"]["temp"] - 273.15
        return round(celsius_temp)

    raise HTTPException(status_code=weather["cod"], detail=weather["message"])


async def get_temperature_for_all_cities(db: Session):
    cities = db.query(DBCity).all()
    data = [get_city_current_temperature(city.name) for city in cities]
    temperatures = await asyncio.gather(*data)
    return zip(cities, temperatures)


async def update_or_create_temperature(
        db: Session, city_id: int, temperature: int
) -> None:
    old_temperature = db.query(DBTemperature).filter(
        DBTemperature.city_id == city_id
    ).first()

    if old_temperature:
        db.execute(
            update(DBTemperature)
            .where(DBTemperature.city_id == city_id)
            .values(temperature=temperature, date_time=datetime.now())
        )
    else:
        new = DBTemperature(
            city_id=city_id,
            temperature=temperature,
            date_time=datetime.now()
        )
        db.add(new)

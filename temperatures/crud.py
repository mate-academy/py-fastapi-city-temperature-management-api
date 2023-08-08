import datetime
import os

from fastapi import HTTPException
from sqlalchemy.orm import Session
import httpx
from dotenv import load_dotenv

import models

load_dotenv()

API_KEY = os.environ.get("API_KEY")


async def update_temperatures(db: Session, city: models.City):
    url = f"https://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city.name}&aqi=no"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)

        db_temperature = models.Temperature(
            city_id=city.id,
            date_time=datetime.datetime.now(),
            temperature=response.json()["current"]["temp_c"]
        )
        db.add(db_temperature)
        db.commit()
        db.refresh(db_temperature)


def get_temperatures(db: Session, city_id: int = None):
    query = db.query(models.Temperature)
    if city_id:
        query = query.filter(city_id == models.Temperature.city_id)

    return query.all()


def get_temperatures_of_city(city_id: int, db: Session):
    db_city = db.query(models.City).filter(models.City.id == city_id)

    if db_city is None:
        raise HTTPException(status_code=400, detail={"error": f"No such city with id {city_id}"})

    temperatures = db.query(models.Temperature).filter(models.Temperature.city_id == city_id).all()

    return temperatures

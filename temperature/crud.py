import os
from datetime import datetime
import httpx
from sqlalchemy.orm import Session
from dotenv import load_dotenv

import models

load_dotenv()

WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY")


async def fetch_temperatures(db: Session, city: models.City):
    url = f"https://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city.name}&aqi=no"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)

        db_temperature = models.Temperature(
            city_id=city.id,
            date_time=datetime.utcnow(),
            temperature=response.json()["current"]["temp_c"]
        )
        db.add(db_temperature)
        db.commit()
        db.refresh(db_temperature)


def get_temperature_by_city_id(
        db: Session,
        city_id: int,
        skip: int = 0,
        limit: int = 100
) -> list[models.Temperature]:
    queryset = db.query(models.Temperature)
    if city_id:
        queryset = queryset.filter(models.Temperature.city_id == city_id)
    return queryset.offset(skip).limit(limit).all()


def get_temperatures(db: Session, skip: int = 0, limit: int = 10) -> list[models.Temperature]:
    return db.query(models.Temperature).offset(skip).limit(limit).all()

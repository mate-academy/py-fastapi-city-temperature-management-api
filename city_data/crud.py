import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session
import httpx
from city_data import models, schemas
from city_data.schemas import CityCreate


def get_city_list(db: Session):
    return db.scalars(select(models.City)).all()


def create_city(db: Session, city_data: CityCreate):
    city = models.City(
        name=city_data.name,
        additional_info=city_data.additional_info,
    )
    db.add(city)
    db.commit()
    db.refresh(city)
    return city


def delete_city(db: Session, city_id: int):
    city = db.scalars(select(models.City).where(models.City.id == city_id)).first()
    if not city:
        return None
    db.delete(city)
    db.commit()
    return city


async def geocode_city(city: str):
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        data = response.json()
    results = data.get("results")
    if not results:
        return None
    res = results[0]
    return res["latitude"], res["longitude"]


async def fetch_temperature(lat: float, lon: float):
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}&current_weather=true"
    )
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()["current_weather"]["temperature"]


def save_temperature(db: Session, city_id: int, temperature_data):
    temperature = models.Temperature(
        city_id=city_id,
        temperature=temperature_data,
        date_time=datetime.datetime.now(),
    )
    db.add(temperature)
    db.commit()
    db.refresh(temperature)
    return temperature


def get_temperature_list(db: Session):
    return db.scalars(select(models.Temperature)).all()


def get_temperature_for_city(db: Session, city_id: int):
    return db.scalars(select(models.Temperature).where(models.Temperature.city_id == city_id)).all()

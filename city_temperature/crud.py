import os

import aiohttp
from dotenv import load_dotenv
from fastapi import HTTPException
from typing import List

from sqlalchemy.orm import Session

from . import models, schemas

load_dotenv()


def create_city(db: Session, city: schemas.CityCreateUpdate) -> models.City:
    db_city = models.City(
        name=city.name,
        additional_info=city.additional_info
    )
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def get_cities(db: Session) -> List[models.City]:
    return db.query(models.City).all()


def get_city(db: Session, city_id: int) -> models.City:
    return db.query(models.City).filter(models.City.id == city_id).first()


def update_city(db: Session, city_id: int, updated_city: schemas.CityCreateUpdate) -> models.City:
    db_city = db.query(models.City).filter(models.City.id == city_id).first()

    if db_city:
        db_city.name = updated_city.name
        db_city.additional_info = updated_city.additional_info

        db.commit()
        db.refresh(db_city)

    return db_city


def delete_city(db: Session, city_id: int) -> None:
    db_city = db.query(models.City).filter(models.City.id == city_id).first()

    db.delete(db_city)
    db.commit()


def get_temperatures(db: Session, city_id: int | None = None) -> List[models.Temperature]:
    queryset = db.query(models.Temperature)

    if city_id is not None:
        queryset = queryset.filter(models.Temperature.city_id == city_id)

    return queryset.all()


def create_temperature(db: Session, temperature: schemas.TemperatureCreateUpdate) -> None:
    db_temperature = (
        db.query(models.Temperature).filter(models.Temperature.city_id == temperature.city_id).first()
    )

    if db_temperature is None:
        db_temperature = models.Temperature(
            temperature=temperature.temperature, city_id=temperature.city_id
        )
        db.add(db_temperature)
    else:
        db_temperature.temperature = temperature.temperature

    db.commit()
    db.refresh(db_temperature)


async def update_temperatures(db: Session) -> None:
    try:
        api_key = os.getenv("API_KEY")

        db_cities = get_cities(db)

        for city in db_cities:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city.name}&appid={api_key}&units=metric"
            response = await fetch_temperature(url)

            temperature = response.get("main", {}).get("temp")
            temperature_data = schemas.TemperatureCreateUpdate(
                city_id=city.id, temperature=temperature
            )
            create_temperature(db=db, temperature=temperature_data)

    except Exception as e:
        print(f"Error fetching temperature data: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch temperature data. Invalid city name",
        )


async def fetch_temperature(url: str) -> None:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response.raise_for_status()
            return await response.json()

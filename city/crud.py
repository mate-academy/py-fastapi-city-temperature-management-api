from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from city import schemas, models
from city.models import City


def get_city(db: Session, limit: int = 20):
    result = db.scalars(select(City).limit(limit))
    return result.all()


def create_city(db: Session, city: schemas.City) -> models.City:
    existing = db.scalar(
        select(models.City).where(
            models.City.additional_info == city.additional_info,
            models.City.name == city.name,
        )
    )
    if existing:
        raise HTTPException(
            status_code=400,
            detail="City with this additional_info already exists"
        )
    db_city = models.City(
        name=city.name,
        additional_info=city.additional_info,
    )
    db.add(db_city)
    db.commit()
    db.refresh(db_city)

    return db_city


def get_city_by_id(db: Session, city_id: int) -> models.City:
    city = db.execute(
        select(models.City).where(models.City.id == city_id)
    ).scalar_one_or_none()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city


def city_update(db: Session, city_id: int, city: schemas.City) -> models.City:
    city_db = get_city_by_id(db, city_id)
    if not city_db:
        raise HTTPException(status_code=404, detail="City not found")

    city_db.name = city.name
    city_db.additional_info = city.additional_info

    db.commit()
    db.refresh(city_db)

    return city_db


def city_delete(db: Session, city_id: int):
    city = db.execute(
        select(models.City).where(models.City.id == city_id)
    ).scalar_one_or_none()
    db.delete(city)
    db.commit()
    return city



import httpx
import os

API_KEY = os.getenv("SECRET_KEY")

async def fetch_temperature(city_name: str) -> float:
    url = "http://api.weatherapi.com/v1/current.json"

    params = {
        "key": API_KEY,
        "q": city_name,
        "aqi": "no"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)

    data = response.json()

    return data["current"]["temp_c"]






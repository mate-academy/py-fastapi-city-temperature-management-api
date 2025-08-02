from datetime import datetime

import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from city_crud_api.schemas import CityUpdate
from models.city_models import City
from models.temperature_models import Temperature
from settings import settings


def get_temperatures_crud(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Temperature).offset(skip).limit(limit).all()

def get_temperature_by_city_id_crud(db: Session, city_id: int):
    return db.query(Temperature).filter(Temperature.city_id == city_id).first()

async def fetch_temperature(city_name: str) -> float:
    url = "http://api.weatherapi.com/v1/current.json"
    params = {
        "key": settings.WEATHER_API_KEY,
        "q": city_name,
        "aqi": "no"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        data = response.json()
        return data["current"]["temp_c"]

async def crud_update_city(db: AsyncSession, city_id: int, city: CityUpdate):
    result = await db.execute(select(City).filter(City.id == city_id))
    db_city = result.scalar_one_or_none()
    if db_city is None:
        return None
    for var, value in city.dict(exclude_unset=True).items():
        setattr(db_city, var, value)
    await db.commit()
    await db.refresh(db_city)
    return db_city

async def crud_update_temperature(db: AsyncSession, city_id: int, temperature: float):
    stmt = select(Temperature).filter(Temperature.city_id == city_id).order_by(Temperature.date_time.desc())
    result = await db.execute(stmt)
    temp_record = result.scalars().first()

    if temp_record:
        # Оновлюємо існуючий запис
        temp_record.temperature = temperature
        temp_record.date_time = datetime.utcnow()
    else:
        # Створюємо новий запис
        temp_record = Temperature(
            city_id=city_id,
            temperature=temperature,
            date_time=datetime.utcnow()
        )
        db.add(temp_record)

    await db.commit()
    await db.refresh(temp_record)
    return temp_record

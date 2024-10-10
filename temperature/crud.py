import os
import httpx
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from starlette import status
from datetime import datetime
from fastapi import HTTPException
from dotenv import load_dotenv
from dependencies import db_dependency
from database.models import Temperature
from temperature.constraints import check_city_temperature_info

load_dotenv()

WEATHER_SECRET_KEY = os.environ.get("OPENWEATHER_SECRET_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


async def get_temperature(city_name: str):
    params = {
        "q": city_name,
        "appid": WEATHER_SECRET_KEY,
        "units": "metric"
    }

    async with httpx.AsyncClient() as Client:
        response = await Client.get(
            BASE_URL,
            params=params
        )
        if response.status_code == status.HTTP_200_OK:
            data = response.json()
            weather_data = {
                "city": data["name"],
                "temperature": data["main"]["temp"]
            }
            return weather_data
        else:
            raise HTTPException(
                detail="City not found",
                status_code=status.HTTP_404_NOT_FOUND
            )


async def record_temperature(db: db_dependency, city_id: int, temperature: float):
    temperature_record = Temperature(
        city_id=city_id,
        date_time=datetime.now(),
        temperature=temperature
    )
    db.add(temperature_record)
    await db.commit()
    await db.refresh(temperature_record)
    return temperature_record


async def get_all_temperatures(db: db_dependency, skip: int = 0, limit: int = 10):
    query = select(Temperature).offset(skip).limit(limit).options(
        joinedload(Temperature.city)
    )
    result = await db.execute(query)
    temperatures_list = result.scalars().all()
    return temperatures_list


async def get_city_temperature(
        db: db_dependency,
        city_id: int,
        skip: int = 0,
        limit: int = 10
):
    city_info = await check_city_temperature_info(db, city_id, skip, limit)
    return city_info

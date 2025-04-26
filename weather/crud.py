import datetime
import os

import httpx
import requests
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

import city.models as city_models
from weather import models, schemas
import dotenv

dotenv.load_dotenv()


async def get_all_weather(db: AsyncSession):
    query = select(models.Weather).options(joinedload(models.Weather.city))
    result = await db.execute(query)
    weather = result.fetchall()
    return [city[0] for city in weather]


async def fetch_weather(city_name: str, base_url: str):
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(f"{base_url}{city_name}")
        response.raise_for_status()  # Raises HTTPError if status is not 200
        return response


async def update_weather(db: AsyncSession) -> dict:
    query = select(city_models.City)
    result = await db.execute(query)
    cities_list = result.fetchall()
    base_url = os.getenv("LINK")
    for city in cities_list:
        weather = await fetch_weather(city[0].name, base_url)
        if weather.status_code == 200:
            weather = weather.json()
            local_time = weather["location"]["localtime"]
            query = insert(models.Weather).values(
                city_id=city[0].id,
                date_time=datetime.datetime.strptime(local_time, '%Y-%m-%d %H:%M'),
                temperature=float(weather["current"]["temp_c"])
            )
            await db.execute(query)
    #commit must be out of the loop
    await db.commit()
    return {"response_line": "Weather updated successfully"}


async def get_one_weather(db: AsyncSession, city_id: int) -> list:
    #here is important thing
    query = select(models.Weather).where(models.Weather.city_id==city_id).options(joinedload(models.Weather.city))
    result = await db.execute(query)
    city = result.fetchone()
    return [city[0]]

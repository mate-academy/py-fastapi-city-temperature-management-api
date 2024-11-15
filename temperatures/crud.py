import os
from datetime import datetime

import httpx
from dotenv import load_dotenv
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from cities import crud
from temperatures import models, schemas

load_dotenv()

API_URL = "http://api.weatherapi.com/v1/current.json"
KEY = os.getenv("API_KEY")


async def get_temperature_from_api(name: str) -> float | None:
    params = {
        "key": KEY,
        "q": name
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(API_URL, params=params)
            response.raise_for_status()
            data = response.json()
            return data["current"]["temp_c"]
        except httpx.HTTPError as e:
            print(f"An error occurred while requesting data: {e}")
            return None


async def create_temperatures_record(
        db: AsyncSession
) -> list[models.Temperature]:
    cities = await crud.get_all_cities(db)
    temperature_records = []
    for city in cities:
        temperature = await get_temperature_from_api(city.name)
        if temperature is not None:
            temperature_record = {
                "city_id": city.id,
                "date_time": datetime.now(),
                "temperature": temperature,
            }
            temperature_records.append(temperature_record)

    if temperature_records:
        statement = insert(models.Temperature).values(
            temperature_records
        ).returning(
            models.Temperature.id,
            models.Temperature.city_id,
            models.Temperature.temperature,
            models.Temperature.date_time
        )
        result = await db.execute(statement)
        await db.commit()
        inserted_records = result.fetchall()
        return [
            schemas.Temperature.model_validate(record)
            for record in inserted_records
        ]


async def get_temperatures_records(
        db: AsyncSession,
        city_id: int | None = None
) -> list[models.Temperature]:
    query = select(models.Temperature)
    print(query)
    if city_id is not None:
        query = query.where(models.Temperature.city_id == city_id)
    result = await db.execute(query)
    print(result)
    return [temp[0] for temp in result.fetchall()]

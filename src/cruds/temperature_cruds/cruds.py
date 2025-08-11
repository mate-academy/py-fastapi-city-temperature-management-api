from typing import List

from httpx import AsyncClient
from sqlalchemy import insert, select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from src import schemas
from src.db import models
from src.settings import Settings


async def get_all(db: AsyncSession):
    query = select(models.Temperature).options(selectinload(models.Temperature.city))

    temperatures_list = await db.execute(query)

    return [
        temperature[0]
        for temperature in temperatures_list.fetchall()
    ]


async def get_by_city_id(city_id: int, db: AsyncSession):
    query = (select(models.Temperature)
             .options(selectinload(models.Temperature.city))
             .where(models.Temperature.city_id == city_id)
             )

    temperatures_list = await db.execute(query)

    return [
        temperature[0]
        for temperature in temperatures_list.fetchall()
    ]



async def get_city_temperature(
        city_name: str,
        http_client: AsyncClient,
        settings: Settings
):
    response = await http_client.get(f"{settings.WTTR_API_ENDPOINT}/{city_name}?format=j1")

    response.raise_for_status()

    data = response.json()

    return data["current_condition"][0]["temp_C"]


async def create_city_temperatures(
        temperatures: List[schemas.TemperatureCreate],
        db: AsyncSession
):
    for temperature in temperatures:
        query = insert(models.Temperature).values(
            date_time=temperature.date_time,
            temperature=temperature.temperature,
            city_id=temperature.city_id
        )

        await db.execute(query)

    await db.commit()

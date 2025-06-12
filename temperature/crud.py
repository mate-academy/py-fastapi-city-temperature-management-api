from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select

from dependencies import fetch_temperature


from temperature import models, schemas
from city.models import City


async def create_temperature(
        db: AsyncSession,
        temperature: schemas.TemperatureCreate
):
    query = insert(models.Temperature).values(
        city_id=temperature.city_id,
        temperature=temperature.temperature,
        date_time=temperature.date_time,
    )
    result = await db.execute(query)
    await db.commit()
    return {**temperature.model_dump(), "id": result.lastrowid}


async def update_temperature(db: AsyncSession):
    cities_result = await db.execute(select(City))
    cities = cities_result.scalars().all()

    updated_cities = []

    for city in cities:
        current_temperature = await fetch_temperature(city.name)

        if current_temperature is None:
            continue

        temperature_data = schemas.TemperatureCreate(
            city_id=city.id,
            temperature=current_temperature,
            date_time=datetime.now(),
        )

        created_record = await create_temperature(
            db=db,
            temperature=temperature_data
        )
        updated_cities.append(created_record)

    await db.commit()
    return updated_cities


async def get_list_of_temperature(db: AsyncSession):
    query = select(models.Temperature).order_by(models.Temperature.date_time)
    temperatures_list = await db.execute(query)
    return [temperatures[0] for temperatures in temperatures_list.fetchall()]


async def get_temperature_by_id(db: AsyncSession, city_id: int):
    query = select(
        models.Temperature
    ).where(
        models.Temperature.city_id == city_id
    ).order_by(models.Temperature.date_time).limit(1)
    res = await db.execute(query)
    db_temperature = res.scalar_one_or_none()
    return db_temperature

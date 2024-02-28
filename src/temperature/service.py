import httpx

from datetime import datetime
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select
from src.config import settings
from src.temperature import models, schemas
from src.city import models as city_models


async def get_temperature_for_city(db: AsyncSession, city_id: int):
    query = select(models.CityTemperature).filter_by(city_id=city_id)

    db_temperature = await db.execute(query)

    temperature = db_temperature.scalar()

    if temperature is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Temperature for city with id '{city_id}' not found"
        )

    return temperature


async def get_all_temperatures(db: AsyncSession, city_id: int | None):
    query = select(models.CityTemperature)

    if city_id:
        query = query.filter_by(city_id=city_id)

    temperatures = await db.execute(query)

    return [temperature[0] for temperature in temperatures.fetchall()]


async def get_weather_for_city(client: httpx.AsyncClient, city_name: str):
    weather_res = await client.get(
        url=settings.CURRENT_WEATHER_URL,
        params={"key": settings.WEATHER_API_KEY, "q": city_name}
    )

    return weather_res.json()


async def create_city_temperature(
        db: AsyncSession,
        temperature: schemas.CityTemperatureCreate
):
    query = insert(models.CityTemperature).values(
        date_time=temperature.date_time,
        temperature=temperature.temperature,
        city_id=temperature.city_id
    )

    await db.execute(query)
    await db.commit()


async def update_city_temperature(
        db: AsyncSession,
        temperature: schemas.CityTemperatureCreate
):
    temperature_db = await get_temperature_for_city(db=db, city_id=temperature.city_id)

    for field, value in temperature.dict(exclude_unset=True).items():
        setattr(temperature_db, field, value)

    await db.merge(temperature_db)

    await db.commit()

    await db.refresh(temperature_db)

    return temperature_db


async def update_or_create_temperature(
        db: AsyncSession,
        temperature: schemas.CityTemperatureCreate
):
    try:
        await update_city_temperature(
            db=db,
            temperature=temperature
        )
    except HTTPException:
        await create_city_temperature(
            db=db,
            temperature=temperature
        )


async def update_temperature_for_cities(db: AsyncSession):
    query = select(city_models.City)
    city_list = await db.execute(query)
    all_cities = [(city[0].name, city[0].id) for city in city_list.fetchall()]

    async with httpx.AsyncClient() as client:
        for city_name, city_id in all_cities:

            weather = await get_weather_for_city(client=client, city_name=city_name)

            location = weather.get("location")
            current = weather.get("current")

            localtime = location["localtime"]
            date, time = localtime.split()
            year, month, day = date.split("-")
            hour, minute = time.split(":")

            date_time = datetime(
                year=int(year),
                month=int(month),
                day=int(day),
                hour=int(hour),
                minute=int(minute)
            )
            current_temp = int(current["temp_c"])

            await update_or_create_temperature(
                db=db,
                temperature=schemas.CityTemperatureCreate(
                    date_time=date_time,
                    temperature=current_temp,
                    city_id=city_id
                )
            )

    return {"message": "Successfully update temperature info for all cities"}

from datetime import datetime
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
import httpx

from temperature import schemas
from temperature.models import DBTemperature
from city.models import DBCity


async def get_temperatures(db: AsyncSession) -> list[DBTemperature]:
    temperatures = await db.scalars(select(DBTemperature))
    return temperatures.all()


async def create_temperature(
    db: AsyncSession,
    temperature: schemas.TemperatureCreate,
) -> DBTemperature:
    db_temperature = DBTemperature(
        city_id=temperature.city_id,
        temperature=temperature.temperature,
        date_time=temperature.date_time,
    )

    db.add(db_temperature)
    try:
        await db.commit()
        await db.refresh(db_temperature)
    except SQLAlchemyError as error:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Could not save temperature record.",
        ) from error

    return db_temperature


async def get_temperature_by_city_id(
        db: AsyncSession, city_id: int
) -> list[DBTemperature]:
    temperatures = await db.scalars(
        select(DBTemperature).where(DBTemperature.city_id == city_id)
    )
    return temperatures.all()


async def update_temperatures(db: AsyncSession) -> list[DBTemperature]:
    cities = await db.scalars(select(DBCity))

    async with httpx.AsyncClient(timeout=10) as client:
        for city in cities:
            try:
                response = await client.get(
                    "https://geocoding-api.open-meteo.com/v1/search",
                    params={"name": city.name, "count": 1},
                )
                response.raise_for_status()
            except httpx.HTTPError as error:
                raise HTTPException(
                    status_code=502,
                    detail=f"Could not fetch coordinates for {city.name}.",
                ) from error

            data = response.json()
            if "results" in data and len(data["results"]) > 0:
                latitude = data["results"][0]["latitude"]
                longitude = data["results"][0]["longitude"]

                try:
                    weather_results = await client.get(
                        "https://api.open-meteo.com/v1/forecast",
                        params={
                            "latitude": latitude,
                            "longitude": longitude,
                            "current": "temperature_2m",
                        },
                    )
                    weather_results.raise_for_status()
                except httpx.HTTPError as error:
                    raise HTTPException(
                        status_code=502,
                        detail=f"Could not fetch temperature for {city.name}.",
                    ) from error

                weather_data = weather_results.json()
                try:
                    temperature_value = weather_data["current"]["temperature_2m"]
                    date_time = datetime.fromisoformat(
                        weather_data["current"]["time"]
                    )
                except (KeyError, TypeError, ValueError) as error:
                    raise HTTPException(
                        status_code=502,
                        detail=f"Temperature data was invalid for {city.name}.",
                    ) from error

                db_temperature = DBTemperature(
                    city_id=city.id,
                    temperature=temperature_value,
                    date_time=date_time,
                )
                db.add(db_temperature)

                try:
                    await db.commit()
                    await db.refresh(db_temperature)
                except SQLAlchemyError as error:
                    await db.rollback()
                    raise HTTPException(
                        status_code=500,
                        detail=f"Could not save temperature for {city.name}.",
                    ) from error
            else:
                raise HTTPException(
                    status_code=404,
                    detail=f"Coordinates were not found for {city.name}.",
                )

    temperatures = await db.scalars(
        select(DBTemperature).order_by(DBTemperature.date_time.desc())
    )
    return temperatures.all()

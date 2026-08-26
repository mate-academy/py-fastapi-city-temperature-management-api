from collections.abc import Sequence
from datetime import datetime, timezone

import httpx
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from city_api import models as city_models
from temperature_api import models, schemas


async def get_all_temperature(db: AsyncSession) -> Sequence[models.Temperature]:
    db_temperature = await db.scalars(select(models.Temperature))
    return db_temperature.all()


async def get_temperature_by_id(db: AsyncSession, temperature_id: int) -> models.Temperature | None:
    db_temperature = await db.scalar(select(models.Temperature).where(models.Temperature.id == temperature_id))
    return db_temperature


async def get_temperature_by_city_id(db: AsyncSession, city_id: int) -> Sequence[models.Temperature] | None:
    return (await db.scalars(
        select(models.Temperature)
        .where(models.Temperature.city_id == city_id))
    ).all()


async def create_temperature(db: AsyncSession, temperature: schemas.Temperature) -> models.Temperature:
    db_temperature = models.Temperature(**temperature.model_dump())
    db.add(db_temperature)

    try:
        await db.commit()
    except IntegrityError as e:
        await db.rollback()
        raise ValueError(f"Temperature with id {temperature.id} already exists") from e

    await db.refresh(db_temperature)
    return db_temperature


async def update_temperature(
        db: AsyncSession,
        temperature_update: schemas.TemperatureUpdate,
        db_temperature: models.Temperature
) -> models.Temperature:
    update_data = temperature_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(db_temperature, field, value)

    try:
        await db.commit()
    except IntegrityError as e:
        await db.rollback()
        raise ValueError(f"Temperature with id {db_temperature.id} already exists") from e

    await db.refresh(db_temperature)
    return db_temperature

async def delete_temperature(db: AsyncSession, db_temperature: models.Temperature) -> None:
    await db.delete(db_temperature)
    await db.commit()


async def _geocode_city(
        client: httpx.AsyncClient,
        city_name: str
) -> tuple[float, float]:
    response = await client.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={"name": city_name, "count": 1},
    )

    response.raise_for_status()
    data = response.json()

    results = data.get("results")
    if not results:
        raise ValueError(f"City {city_name} not found")

    location = results[0]
    return location["latitude"], location["longitude"]


async def _fetch_temperature(
        client:httpx.AsyncClient,
        city_name: str,
):
    latitude, longitude = await _geocode_city(client=client, city_name=city_name)

    response = await client.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m",
        }
    )
    response.raise_for_status()
    data = response.json()
    return data["current"]["temperature_2m"]


async def update_all_temperatures(db: AsyncSession) -> list[models.Temperature]:
    cities = (await db.scalars(select(city_models.City))).all()

    created: list[models.Temperature] = []

    async with httpx.AsyncClient() as client:
        for city in cities:
            temp_value = await _fetch_temperature(client, city.name)
            db_temperature = models.Temperature(
                city_id=city.id,
                date_time=datetime.now(timezone.utc),
                temperature=temp_value,
            )
            db.add(db_temperature)
            created.append(db_temperature)

    await db.commit()

    for db_temperature in created:
        await db.refresh(db_temperature)

    return created

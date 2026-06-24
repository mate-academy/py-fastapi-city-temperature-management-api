from datetime import datetime, timezone

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.annotation import Annotated

from app import models, schemas
from app.database import get_db


async def create_city(
        db: Annotated[AsyncSession, Depends(get_db)],
        city: schemas.CityCreate
) -> models.City:
    db_city = models.City(**city.model_dump())
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)
    return db_city


async def get_cities(
        db: Annotated[AsyncSession, Depends(get_db)]
) -> list[models.City]:
    result = await db.execute(select(models.City).order_by(models.City.id))
    return list(result.scalars().all())


async def get_city(
        db: Annotated[AsyncSession, Depends(get_db)],
        city_id: int
) -> models.City | None:
    return await db.get(models.City, city_id)


async def delete_city(
        db: Annotated[AsyncSession, Depends(get_db)],
        city: models.City
) -> None:
    await db.delete(city)
    await db.commit()


async def create_temperatures(
    db: Annotated[AsyncSession, Depends(get_db)],
    city_temperatures: list,
) -> list[models.Temperature]:
    recorded_at = datetime.now(timezone.utc)
    records = [
        models.Temperature(
            city_id=city_id,
            date_time=recorded_at,
            temperature=temperature,
        )
        for city_id, temperature in city_temperatures
    ]
    db.add_all(records)
    await db.commit()

    for record in records:
        await db.refresh(record)

    return records


async def get_temperatures(
    db: Annotated[AsyncSession, Depends(get_db)],
    city_id: int | None = None,
) -> list[models.Temperature]:
    query = select(models.Temperature).order_by(
        models.Temperature.date_time.desc()
    )
    if city_id is not None:
        query = query.where(models.Temperature.city_id == city_id)

    result = await db.execute(query)
    return list(result.scalars().all())

from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
import models, schemas


async def get_all_cities(db: AsyncSession) -> list[models.DBCity]:
    cities = await db.scalars(select(models.DBCity))
    return cities.all() # type: ignore

async def get_city_by_id(db: AsyncSession, city_id: int) -> models.DBCity | None:
    return await db.scalar(
        select(models.DBCity).where(models.DBCity.id == city_id)
    )

async def create_city(db: AsyncSession, city: schemas.CityCreate) -> models.DBCity:
    db_city = models.DBCity(
        name = city.name,
        additional_info = city.additional_info,
    )
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)
    return db_city

async def get_city_by_name(
    db: AsyncSession,
    name: str
) -> models.DBCity | None:
    return await db.scalar(
        select(
            models.DBCity
        ).where(
            models.DBCity.name == name
        )
    )


async def update_city(
        db: AsyncSession,
        city_id: int,
        new_data: schemas.CityCreate,
) ->  models.DBCity | None:
    db_city = await get_city_by_id(db, city_id)
    if db_city is None:
        return None
    
    db_city.name = new_data.name
    db_city.additional_info = new_data.additional_info

    await db.commit()
    await db.refresh(db_city)
    return db_city

async def delete_city(db: AsyncSession, city_id: int) ->  models.DBCity | None:
    db_city = await get_city_by_id(db, city_id)
    if db_city is None:
        return None
    
    await db.delete(db_city)
    await db.commit()
    return db_city

async def get_temperature_list(
    db: AsyncSession,
    city_id: int | None = None,
) -> list[models.DBTemperature]:

    stmt = select(models.DBTemperature).options(
        joinedload(models.DBTemperature.city)
    )

    if city_id is not None:
        stmt = stmt.where(models.DBTemperature.city_id == city_id)

    result = await db.scalars(stmt)
    return result.all() # type: ignore

async def create_temperature(
        db: AsyncSession,
        city_id: int,
        temperature: float
    ) -> models.DBTemperature | None:
    db_temperature = models.DBTemperature(
        city_id = city_id,
        date_time=datetime.now(timezone.utc),
        temperature=temperature,
    )

    db.add(db_temperature)

    await db.commit()
    await db.refresh(db_temperature)
    return db_temperature
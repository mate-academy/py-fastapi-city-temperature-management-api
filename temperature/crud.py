import datetime

from fastapi import HTTPException
from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession

from temperature import models


async def get_list_temperatures(
    db: AsyncSession, city_id: int = None, skip: int = 0, limit: int = 100
) -> list[models.Temperature]:
    query = select(models.Temperature)
    if city_id is not None:
        query = query.filter(models.Temperature.city_id == city_id)
    query = query.offset(skip).limit(limit)
    temp_list = await db.execute(query)

    return temp_list.scalars()


async def get_temperature_by_city_id(
    db: AsyncSession, city_id: int
) -> models.Temperature:
    query = select(models.Temperature).filter(
        models.Temperature.city_id == city_id
    )
    temp = await db.execute(query)
    return temp.scalar()


async def create_temperature(
    db: AsyncSession,
    temp: float,
    city_id: int,
) -> models.Temperature:
    query = insert(models.Temperature).values(
        temperature=temp, city_id=city_id, date_time=datetime.datetime.now()
    )
    await db.execute(query)
    await db.commit()


async def update_temperature(
    db: AsyncSession,
    city_id: int,
    temp: float,
) -> models.Temperature:
    db_temp = await get_temperature_by_city_id(db=db, city_id=city_id)
    if db_temp:
        query = (
            update(models.Temperature)
            .where(models.Temperature.city_id == city_id)
            .values(
                temperature=temp,
                date_time=datetime.datetime.now(),
            )
        )
        temp = await db.execute(query)
        await db.commit()
        if temp.rowcount == 1:
            return db_temp

    raise HTTPException(status_code=404, detail="City not found")

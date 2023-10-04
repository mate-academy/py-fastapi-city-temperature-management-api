import asyncio
import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from temperature import models


async def get_list_temperatures(
    db: AsyncSession, city_id: int = None, skip: int = 0, limit: int = 100
) -> list[models.Temperature]:
    query = select(models.Temperature).offset(skip).limit(limit)
    if city_id is not None:
        query = query.filter(models.Temperature.city_id == city_id)

    temp_list = await db.execute(query)
    return [temp[0] for temp in temp_list.fetchall()]


async def get_temperature_by_city_id(
    db: AsyncSession, city_id: int
) -> models.Temperature:
    query = select(models.Temperature).filter(
        models.Temperature.city_id == city_id
    )
    temp = await db.execute(query)
    return temp.scalar()


def create_temperature(
    db: Session,
    temp: float,
    city_id: int,
) -> models.Temperature:
    db_temp = models.Temperature(
        temperature=temp,
        city_id=city_id,
        date_time=datetime.datetime.now(),
    )

    db.add(db_temp)
    db.commit()
    db.refresh(db_temp)

    return db_temp


# def update_temperature(
#     db: Session,
#     city_id: int,
#     temp: float,
# ) -> models.Temperature:
#     db_temp = (
#         db.query(models.Temperature)
#         .filter(models.Temperature.city_id == city_id)
#         .first()
#     )
#     if db_temp:
#         db_temp.temperature = temp
#         db_temp.date_time = datetime.datetime.now()
#         db.commit()
#         db.refresh(db_temp)
#         return db_temp

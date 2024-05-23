from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession
import datetime

from . import models
from .openweather import get_temperature


async def get_all_degrees(db: AsyncSession,
                          skip: int = 0,
                          limit: int = 10) -> list | None:
    query = select(models.DBTemperature).offset(skip).limit(limit)
    degrees_list = await db.execute(query)
    return [degree[0] for degree in degrees_list.fetchall()]


async def get_degrees_by_city_id(
        db: AsyncSession,
        city_id: int,
        skip: int = 0, limit: int = 10
) -> list | None:
    query = (select(models.DBTemperature).
             offset(skip).limit(limit).
             where(models.DBTemperature.city_id == city_id))
    degrees = await db.execute(query)
    return [degree[0] for degree in degrees.fetchall()]


async def clear_degrees_for_city_id(
        db: AsyncSession, city_id: int
) -> dict | None:
    query = delete(models.DBTemperature).where(
        models.DBTemperature.city_id == city_id
    )
    del_degrees = await db.execute(query)
    if del_degrees.rowcount == 0:
        return None
    await db.commit()
    return {"message": f"Successfully deleted to city id: {city_id}"}


async def clear_degrees_all(db: AsyncSession) -> dict | None:
    query = delete(models.DBTemperature)
    del_degrees = await db.execute(query)
    if del_degrees.rowcount == 0:
        return None
    await db.commit()
    return {
        "message": f"Successfully deleted {del_degrees.rowcount} record(s)"
    }


async def update_degree_by_city(
        db: AsyncSession,
        city_name: str, city_id: int
) -> str | Exception:
    temperature = await get_temperature(city_name.capitalize())
    if isinstance(temperature, str):
        return temperature
    date_time = datetime.datetime.now(datetime.UTC)
    query = insert(models.DBTemperature).values(
        city_id=city_id, date_time=date_time, temperature=temperature
    )

    await db.execute(query)
    await db.commit()

    return (f"{date_time.strftime("%d/%m/%Y %H:%M:%S")}UTC - "
            f"current temperature value in {city_name.capitalize()} "
            f"was added to the database")

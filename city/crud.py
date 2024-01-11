from fastapi import HTTPException
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from . import models, schemas


async def get_all_city(db: AsyncSession) -> list[dict]:
    query = select(models.DBCity)
    city_list = await db.execute(query)
    return [city[0] for city in city_list.fetchall()]


async def create_city(db: AsyncSession, city: schemas.CityCreate) -> dict:
    query = insert(models.DBCity).values(
        name=city.name,
        additional_info=city.additional_info
    )
    result = await db.execute(query)
    await db.commit()
    resp = {**city.model_dump(), "id": result.lastrowid}
    return resp


async def check_city_in_db(db: AsyncSession, city_id: int) -> None:
    query = select(models.DBCity).where(models.DBCity.id == city_id)
    city = await db.execute(query)

    if city.scalar() is None:
        raise HTTPException(status_code=404, detail="City not found")


async def get_city(db: AsyncSession, city_id: int) -> dict:
    await check_city_in_db(db=db, city_id=city_id)
    query = select(models.DBCity).where(models.DBCity.id == city_id)
    city = await db.execute(query)
    return city.scalar()


async def update_city(db: AsyncSession, city_id: int, city: schemas.CityCreate) -> None:
    await check_city_in_db(db=db, city_id=city_id)
    query = update(models.DBCity).where(models.DBCity.id == city_id).values(
        name=city.name,
        additional_info=city.additional_info
    )
    await db.execute(query)
    await db.commit()


async def delete_city(db: AsyncSession, city_id: int) -> None:
    await check_city_in_db(db=db, city_id=city_id)
    query = delete(models.DBCity).where(models.DBCity.id == city_id)
    await db.execute(query)
    await db.commit()

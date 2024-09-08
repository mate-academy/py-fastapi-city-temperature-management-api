from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from city import schemas
from city.models import DBCity


async def get_cities_list(
    db: AsyncSession, skip: int = 0, limit: int = 10
) -> list[DBCity]:
    result = await db.execute(select(DBCity).offset(skip).limit(limit))
    return result.scalars().all()


async def get_city_by_id(db: AsyncSession, city_id: int) -> Optional[DBCity]:
    result = await db.execute(select(DBCity).filter(DBCity.id == city_id))
    return result.scalars().first()


async def create_city(db: AsyncSession, city: schemas.CityCreate) -> DBCity:
    existing_city_query = select(DBCity).filter(DBCity.name == city.name)
    result = await db.execute(existing_city_query)
    existing_city = result.scalars().first()

    if existing_city:
        raise ValueError("City with this name already exists")

    db_city = DBCity(
        name=city.name,
        additional_info=city.additional_info,
    )
    db.add(db_city)
    try:
        await db.commit()
        await db.refresh(db_city)
    except IntegrityError:
        await db.rollback()
        raise
    return db_city


async def update_city_by_id(
    db: AsyncSession, city_id: int, city: schemas.CityUpdate
) -> Optional[DBCity]:
    db_city = await get_city_by_id(db=db, city_id=city_id)
    if db_city:
        if city.name:
            db_city.name = city.name
        if city.additional_info:
            db_city.additional_info = city.additional_info
        await db.commit()
        await db.refresh(db_city)
    return db_city


async def delete_city_by_id(db: AsyncSession, city_id: int) -> Optional[DBCity]:
    db_city = await get_city_by_id(db=db, city_id=city_id)
    if db_city:
        await db.delete(db_city)
        await db.commit()
    return db_city

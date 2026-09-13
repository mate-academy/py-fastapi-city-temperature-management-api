from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ..models.city_model import DBCity

from app.schemas import city_schema


async def get_all_cities(db: AsyncSession) -> list[DBCity]:
    cities = await db.scalars(select(DBCity).
                              options(selectinload(DBCity.temperatures)))
    return cities.all()


async def create_city(
        db: AsyncSession,
        city: city_schema.CityCreate
) -> DBCity:
    db_city = DBCity(
        name=city.name,
        additional_info=city.additional_info,
    )
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)

    return db_city


async def get_city_by_name(db: AsyncSession, name: str) -> DBCity:
    db_city = await db.scalars(select(DBCity).where(DBCity.name == name))
    return db_city.one_or_none()


async def get_city_by_id(db: AsyncSession, city_id: int) -> DBCity:
    db_city = await db.scalars(select(DBCity).where(DBCity.id == city_id))
    return db_city.one_or_none()


async def update_city(
    db: AsyncSession, city_id: int, city: city_schema.CityCreate
) -> DBCity:

    db_city = await db.get(DBCity, city_id)

    db_city.name = city.name
    db_city.additional_info = city.additional_info

    await db.commit()
    await db.refresh(db_city)

    return db_city


async def delete_city(db: AsyncSession, city: DBCity):
    await db.delete(city)
    await db.commit()

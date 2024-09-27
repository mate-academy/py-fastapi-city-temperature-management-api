from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload, noload

from City_app.models import DBCity
from City_app.schemas import CityCreate


STMT = (
    select(DBCity)
    .options(selectinload(DBCity.temperatures))
    .order_by(DBCity.name)
)


async def get_all_cities_with_temperatures(db: AsyncSession) -> List[DBCity]:
    cities = await db.scalars(STMT)
    return list(cities)


async def get_all_cities(db: AsyncSession) -> List[DBCity]:
    stmt = (
        select(DBCity)
        .options(noload(DBCity.temperatures))
        .order_by(DBCity.name)
    )
    cities = await db.scalars(stmt)
    return list(cities)


async def get_city_with_temperatures(db: AsyncSession, city_id: int) -> DBCity | None:
    stmt = STMT.where(DBCity.id == city_id)
    city = await db.scalar(stmt)
    return city


async def create_city(db: AsyncSession, city_data: CityCreate) -> DBCity:
    city = DBCity(**city_data.dict())
    db.add(city)

    await db.commit()
    await db.refresh(city)

    city = await get_city_with_temperatures(db, city.id)

    return city


async def update_city(
        db: AsyncSession,
        city_id: int,
        city_data: CityCreate
) -> DBCity:
    city = await get_city_with_temperatures(db=db, city_id=city_id)
    if city is not None:
        city.name = city_data.name
        city.additional_info = city_data.additional_info
        await db.commit()
        await db.refresh(city)

        return city


async def delete_city(
        db: AsyncSession,
        city_id: int
):
    city = await get_city_with_temperatures(db=db, city_id=city_id)

    if city is not None:
        await db.delete(city)
        await db.commit()

        return city

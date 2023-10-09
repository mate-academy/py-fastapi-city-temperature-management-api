from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from city import schemas
from city.models import DBCity


async def get_all_cities(
     db: AsyncSession,
     skip: int = 0,
     limit: int = 10
) -> List[schemas.City]:
    query = select(DBCity).offset(skip).limit(limit)
    cities = await db.execute(query)

    return [city[0] for city in cities.fetchall()]


async def get_city_by_id(
     db: AsyncSession,
     city_id: int
) -> schemas.CityDetail:
    query = select(DBCity).where(
     DBCity.id == city_id
    ).options(joinedload(DBCity.temperatures))
    city = await db.execute(query)
    return city.scalar()


async def post_city(
     db: AsyncSession,
     city: schemas.CityCreate
) -> schemas.City:
    query = select(DBCity).where(
        DBCity.name == city.name
    )
    check_unique_name = await db.execute(query)
    if not check_unique_name.scalar():
        new_city = DBCity(**city.model_dump())
        db.add(new_city)
        await db.commit()
        await db.refresh(new_city)
        return new_city


async def update_city(
     db: AsyncSession,
     city_id: int,
     updated_city: schemas.CityUpdate
) -> schemas.CityDetail:
    city = await get_city_by_id(db, city_id)

    if city:
        for attr, value in updated_city.model_dump().items():
            setattr(city, attr, value)

        await db.commit()
        await db.refresh(city)

    return city


async def delete_city(db: AsyncSession,
                      city_id: int) -> schemas.CityDetail:
    city = await get_city_by_id(db, city_id)

    if city:
        await db.delete(city)
        await db.commit()

    return city

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from city import schemas
from city import models


async def get_cities(db: AsyncSession):
    result = await db.execute(select(models.City))
    cities = result.scalars().all()

    return cities


async def check_city_name_exists(db: AsyncSession, city_name: str):
    result = await db.execute(
        select(models.City).filter(models.City.name == city_name)
    )
    return result.scalar()


async def get_city_by_id(db: AsyncSession, city_id: int):
    result = await db.get(models.City, city_id)
    return result


async def create_city(db: AsyncSession, city: schemas.CityCreate):
    db_city = models.City(
        name=city.name,
        additional_info=city.additional_info
    )

    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)

    return db_city


async def delete_city(db: AsyncSession, city_id: int):
    city_to_delete = await get_city_by_id(db, city_id)

    if city_to_delete:
        await db.delete(city_to_delete)
        await db.commit()
        return "City deleted"
    else:
        return "City not found"

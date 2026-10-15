from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from cities.models import City
from cities import schemas


async def create_city(db: AsyncSession, city: schemas.CityCreate) -> City:
    db_city = City(name=city.name, additional_info=city.additional_info)
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)
    return db_city


async def get_cities(db: AsyncSession) -> list[City]:
    result = await db.scalars(select(City))
    return list(result.all())


async def get_city(db: AsyncSession, city_id: int) -> City | None:
    result = await db.scalars(
        select(City)
        .where(City.id == city_id)
        .options(selectinload(City.temperatures))
    )
    return result.one_or_none()


async def get_city_by_name(db: AsyncSession, name: str) -> City | None:
    return await db.scalar(select(City).where(City.name == name))


async def update_city(
    db: AsyncSession, db_city: City, city_data: schemas.CityUpdate
) -> City:
    for key, value in city_data.model_dump().items():
        setattr(db_city, key, value)

    await db.commit()
    await db.refresh(db_city)
    return db_city


async def delete_city(db: AsyncSession, db_city: City) -> None:
    await db.delete(db_city)
    await db.commit()

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from cities.models import City
from cities.schemas import CityCreate, CityUpdate


async def get_single_city_by_name(
        db: AsyncSession,
        name: str
    )  -> City | None:
    statement = select(City).where(City.name == name)
    result = await db.execute(statement)

    return result.scalar_one_or_none()


async def create_city(
        db: AsyncSession,
        city: CityCreate
) -> City:
    db_city = City(
        name=city.name,
        additional_info=city.additional_info
    )
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)

    return db_city


async def update_city(
        db: AsyncSession,
        city: CityUpdate,
        db_city: City
):
    db_city.name = city.name
    db_city.additional_info = city.additional_info

    await db.commit()
    await db.refresh(db_city)

    return db_city


async def get_cities(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 10,
) -> list[City]:
    statement = select(City).offset(skip).limit(limit)
    result = await db.execute(statement)

    return list(result.scalars().all())


async def get_city_by_id(
    db: AsyncSession,
    city_id: int,
) -> City | None:

    statement = select(City).where(City.id == city_id)
    result = await db.execute(statement)

    return result.scalar_one_or_none()


async def delete_city_by_id(
    db: AsyncSession,
    db_city: City
) -> bool:
    await db.delete(db_city)
    await db.commit()

    return True

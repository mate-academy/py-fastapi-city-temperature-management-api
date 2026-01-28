from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from models.city import City
from schemas.city import CityCreateSchema

from .exceptions import CityAlreadyExistsException


async def get_all_cities(db: AsyncSession) -> list[City]:
    result = await db.execute(select(City))
    return result.scalars().all()


async def get_city_by_id(db: AsyncSession, city_id: int) -> City | None:
    result = await db.execute(
        select(City).where(City.id == city_id)
    )
    return result.scalars().one_or_none()


async def create_city(db: AsyncSession, city_in: CityCreateSchema) -> City:
    if await db.execute(
        select(City).where(City.name == city_in.name)
    ).scalars().first():
        raise CityAlreadyExistsException(city_in.name)

    city = City(**city_in.model_dump())
    db.add(city)
    await db.commit()
    await db.refresh(city)
    return city


async def update_city(
    db: AsyncSession,
    city_id: int,
    city_update: CityCreateSchema
) -> City | None:
    city = await get_city_by_id(db, city_id)
    if not city:
        return None

    for key, value in city_update.model_dump(exclude_unset=True).items():
        setattr(city, key, value)

    await db.commit()
    await db.refresh(city)
    return city


async def delete_city(db: AsyncSession, city_id: int) -> bool:
    result = await db.execute(
        delete(City).where(City.id == city_id)
    )
    await db.commit()
    return result.rowcount > 0

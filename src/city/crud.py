from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.city.models import DBCity
from src.city.schemas import CityCreateSchema


async def create_city(db: AsyncSession, city_data: CityCreateSchema) -> DBCity:
    db_city = DBCity(**city_data.model_dump())

    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)

    return db_city


async def get_cities(db: AsyncSession) -> list[DBCity]:
    result = await db.scalars(select(DBCity))
    return list(result.all())


async def get_city_by_id(db: AsyncSession, city_id: int) -> DBCity | None:
    return await db.scalar(select(DBCity).where(DBCity.id == city_id))


async def update_city_by_id(
        db: AsyncSession,
        city_id: int,
        name: str,
        additional_info: str
) -> DBCity | None:
    db_city = await get_city_by_id(db, city_id)

    if db_city:
        db_city.name = name
        db_city.additional_info = additional_info
        await db.commit()
        await db.refresh(db_city)
        return db_city

    return None


async def delete_city(db: AsyncSession, city_id: int) -> DBCity | None:
    db_city = await get_city_by_id(db, city_id)

    if db_city:
        await db.delete(db_city)
        await db.commit()
        return db_city

    return None

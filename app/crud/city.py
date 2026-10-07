from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import DBCity
from app.schemas.city import CityCreate, CityUpdate


async def get_cities(db: AsyncSession) -> list[DBCity]:
    result = await db.execute(select(DBCity))
    return list(result.scalars().all())


async def get_city(db: AsyncSession, city_id: int) -> DBCity | None:
    return await db.get(DBCity, city_id)


async def create_city(db: AsyncSession, city: CityCreate) -> DBCity:
    db_city = DBCity(**city.model_dump())
    db.add(db_city)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise
    await db.refresh(db_city)
    return db_city


async def update_city(
        db: AsyncSession,
        db_city: DBCity,
        city: CityUpdate,
) -> DBCity:
    for field, value in city.model_dump(exclude_unset=True).items():
        setattr(db_city, field, value)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise
    await db.refresh(db_city)
    return db_city


async def delete_city(db: AsyncSession, db_city: DBCity) -> None:
    await db.delete(db_city)
    await db.commit()

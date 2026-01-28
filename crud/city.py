from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.models import DBCity
from schemas.city import CityCreate, City


async def get_all_cities(db: AsyncSession):
    result = await db.scalars(select(DBCity))

    return list(result.all())


async def create_city(db: AsyncSession, city_data: CityCreate):
    db_city = DBCity(**city_data.model_dump())
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)

    return db_city


async def get_city_by_id(db: AsyncSession, city_id: int):
    result = await db.execute(select(DBCity).where(DBCity.id == city_id))
    return result.scalar_one_or_none()


async def delete_city(db: AsyncSession, city_id: int) -> bool:
    db_city = await get_city_by_id(db, city_id)
    if not db_city:
        return False
    await db.delete(db_city)
    await db.commit()
    return True

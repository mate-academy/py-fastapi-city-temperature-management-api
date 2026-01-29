from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.city import City


async def create_city(db: AsyncSession, name: str, info: str | None):
    city = City(name=name, additional_info=info)
    db.add(city)
    await db.commit()
    await db.refresh(city)
    return city


async def get_cities(db: AsyncSession):
    result = await db.execute(select(City))
    return result.scalars().all()


async def get_city(db: AsyncSession, city_id: int):
    result = await db.execute(select(City).where(City.id == city_id))
    return result.scalar_one_or_none()


async def delete_city(db: AsyncSession, city: City):
    await db.delete(city)
    await db.commit()

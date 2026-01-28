from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from city.models import City


async def create_city(db: AsyncSession, data: City):
    db.add(data)
    await db.commit()
    await db.refresh(data)
    return data


async def get_all_cities(db: AsyncSession):
    result = await db.scalars(select(City))
    return result.all()


async def delete_city(db: AsyncSession, city_id: int):
    city = await db.get(City, city_id)
    if not city:
        return None
    await db.delete(city)
    await db.commit()
    return city
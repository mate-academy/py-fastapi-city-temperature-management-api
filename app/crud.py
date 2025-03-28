from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import City, Temperature


async def create_city(db: AsyncSession, name: str, additional_info: str):
    city = City(name=name, additional_info=additional_info)
    db.add(city)
    await db.commit()
    await db.refresh(city)
    return city

async def get_cities(db: AsyncSession):
    result = await db.execute(select(City))
    return result.scalars().all()

async def delete_city(db: AsyncSession, city_id: int):
    city = await db.get(City, city_id)
    if city:
        await db.delete(city)
        await db.commit()
        return True
    return False

async def create_temperature(db: AsyncSession, city_id: int, temperature: float):
    temp = Temperature(city_id=city_id, temperature=temperature)
    db.add(temp)
    await db.commit()
    await db.refresh(temp)
    return temp

async def get_temperatures(db: AsyncSession, city_id: int = None):
    query = select(Temperature)
    if city_id:
        query = query.where(Temperature.city_id == city_id)
    result = await db.execute(query)
    return result.scalars().all()

# crud.py
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from models import City

async def create_city(session: AsyncSession, city: City) -> City:
    session.add(city)
    await session.commit()
    await session.refresh(city)
    return city

async def get_cities(session: AsyncSession) -> List[City]:
    result = await session.execute(
        "SELECT * FROM cities"
    )
    return result.scalars().all()

async def delete_city(session: AsyncSession, city_id: int):
    db_city = await session.get(City, city_id)
    if not db_city:
        raise ValueError("City not found")
    await session.delete(db_city)
    await session.commit()

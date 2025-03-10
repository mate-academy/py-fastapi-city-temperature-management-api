from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from cities.models import City
from cities.schemas import CityCreate


async def create_city(db: AsyncSession, city_data: CityCreate) -> City:
    new_city = City(**city_data.model_dump())
    db.add(new_city)
    try:
        await db.commit()
        await db.refresh(new_city)
        return new_city
    except IntegrityError:
        await db.rollback()
        raise ValueError("City with this name already exists")


async def get_cities(db: AsyncSession):
    result = await db.execute(select(City))
    return result.scalars().all()


async def delete_city(db: AsyncSession, city_id: int) -> bool:
    city = await db.get(City, city_id)
    if city:
        await db.delete(city)
        await db.commit()
        return True
    return False

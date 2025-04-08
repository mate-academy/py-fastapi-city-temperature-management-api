from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.city import City
from app.schemas.city import CityCreate

async def get_all_cities(db: AsyncSession):
    result = await db.execute(select(City))
    return result.scalars().all()

async def create_city(db: AsyncSession, city: CityCreate):
    db_city = City(**city.dict())
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)
    return db_city

async def delete_city(db: AsyncSession, city_id: int):
    city = await db.get(City, city_id)
    if city:
        await db.delete(city)
        await db.commit()
    return city

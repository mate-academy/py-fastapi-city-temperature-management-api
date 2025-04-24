from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import models
from city import schemas

async def create_city(db: AsyncSession, city: schemas.CityCreate):
    db_city = models.City(**city.dict())
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)
    return db_city

async def get_cities(db: AsyncSession):
    result = await db.execute(select(models.City))
    return result.scalars().all()

async def get_city(db: AsyncSession, city_id: int):
    result = await db.execute(select(models.City).where(models.City.id == city_id))
    return result.scalars().first()

async def update_city(db: AsyncSession, city_id: int, city: schemas.CityUpdate):
    result = await db.execute(select(models.City).where(models.City.id == city_id))
    db_city = result.scalars().first()
    if not db_city:
        return None
    for var, value in city.dict(exclude_unset=True).items():
        setattr(db_city, var, value)
    await db.commit()
    await db.refresh(db_city)
    return db_city

async def delete_city(db: AsyncSession, city_id: int):
    result = await db.execute(select(models.City).where(models.City.id == city_id))
    db_city = result.scalars().first()
    if not db_city:
        return None
    await db.delete(db_city)
    await db.commit()
    return db_city
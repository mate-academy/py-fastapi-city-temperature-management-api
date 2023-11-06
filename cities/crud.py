from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from cities import schemas, models


async def read_cities(db: AsyncSession, skip: int = 0, limit: int = 50):
    stmt = select(models.City).offset(skip).limit(limit)
    return await db.scalars(stmt)


async def read_city(db: AsyncSession, city_id: int):
    stmt = select(models.City).where(models.City.id == city_id)
    return (await db.scalars(stmt)).first()


async def create_city(db: AsyncSession, city: schemas.CityCreate):
    db_city = models.City(**city.model_dump())
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)
    return db_city


async def update_city(
    db: AsyncSession, city_id: int, city: schemas.CityUpdate
):
    db_city = await read_city(city_id=city_id, db=db)
    if db_city is None:
        return None

    for attr_name, value in city.model_dump().items():
        setattr(db_city, attr_name, value)

    await db.commit()
    await db.refresh(db_city)

    return db_city


async def delete_city(db: AsyncSession, city_id: int):
    db_city = await read_city(city_id=city_id, db=db)
    if db_city is None:
        return False

    await db.delete(db_city)
    await db.commit()

    return True

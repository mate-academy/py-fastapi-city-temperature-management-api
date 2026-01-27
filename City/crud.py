from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from City.models import City
from City import schemas


async def get_city_by_name(db: AsyncSession, name: str):
    return await db.scalar(select(City).where(City.name == name))

async def get_city(db: AsyncSession, city_id: int):
    return await db.scalar(select(City).where(City.id == city_id))

async def get_cities(db: AsyncSession):
    query = await db.scalars(select(City))
    return query.all()

async def create_city(db: AsyncSession, city_data: schemas.CreateCitySchema):
    db_city = City(**city_data.model_dump())
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)
    return db_city

async def update_city(db: AsyncSession, city_id: int, city_data: schemas.UpdateCitySchema):
    query = await db.execute(select(City).where(City.id == city_id))
    db_city = query.scalar_one_or_none()

    if db_city:
        update_data = city_data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(db_city, key, value)

        await db.commit()
        await db.refresh(db_city)

    return db_city


async def delete_city(db: AsyncSession, city_id: int):
    query = select(City).where(City.id == city_id)
    result = await db.execute(query)
    db_city = result.scalar_one_or_none()

    if db_city:
        await db.delete(db_city)
        await db.commit()
        return db_city
    return None

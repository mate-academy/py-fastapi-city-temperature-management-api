from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.cities.models import CityModel
from app.cities.schemas import CityCreate, CityUpdate


async def get_all_cities(db: AsyncSession):
    result = await db.execute(select(CityModel))
    return result.scalars().all()


async def get_city_by_id(db: AsyncSession, city_id: int):
    result = await db.execute(select(CityModel).filter(CityModel.id == city_id))
    return result.scalar_one_or_none()


async def get_city_by_name(db: AsyncSession, name: str):
    result = await db.execute(select(CityModel).filter(CityModel.name == name))
    return result.scalar_one_or_none()


async def create_city(db: AsyncSession, city_data: CityCreate):
    db_city = CityModel(**city_data.model_dump())
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)
    return db_city


async def update_city(db: AsyncSession, db_city: CityModel, update_data: CityUpdate):
    data = update_data.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(db_city, key, value)
    await db.commit()
    await db.refresh(db_city)
    return db_city


async def delete_city(db: AsyncSession, db_city: CityModel):
    await db.delete(db_city)
    await db.commit()

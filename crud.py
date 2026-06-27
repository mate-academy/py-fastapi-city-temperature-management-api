import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import CityModel, TemperatureModel
from schemas import CityCreate, CityPartialUpdate


async def get_all_cities(db: AsyncSession):
    result = await db.execute(select(CityModel))
    return result.scalars().all()


async def get_city(db: AsyncSession, city_id: int):
    result = await db.execute(select(CityModel).where(CityModel.id == city_id))
    return result.scalars().first()


async def create_city(db: AsyncSession, city: CityCreate):
    db_city = CityModel(**city.model_dump())
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)
    return db_city


async def patch_city(db: AsyncSession, city_id: int, city: CityPartialUpdate):
    db_city = await get_city(db, city_id)
    if not db_city:
        return None

    update_data = city.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_city, field, value)

    await db.commit()
    await db.refresh(db_city)
    return db_city


async def delete_city(db: AsyncSession, city_id: int):
    db_city = await get_city(db, city_id)
    if not db_city:
        return None

    await db.delete(db_city)
    await db.commit()
    return db_city


async def get_temperatures(
    db: AsyncSession,
    city_id: int | None = None,
) -> list[TemperatureModel]:
    query = select(TemperatureModel)

    if city_id is not None:
        query = query.where(TemperatureModel.city_id == city_id)

    return list(await db.scalars(query))


async def create_temperature(
    db: AsyncSession,
    city_id: int,
    temperature: float,
) -> TemperatureModel:
    db_temperature = TemperatureModel(
        city_id=city_id,
        temperature=temperature,
        date_time=datetime.datetime.now(),
    )
    db.add(db_temperature)
    await db.commit()
    await db.refresh(db_temperature)
    return db_temperature

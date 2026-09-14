from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import City, Temperature
from app.schemas import CityCreate


async def create_city(
    db: AsyncSession,
    city_data: CityCreate,
) -> City:
    city = City(
        name=city_data.name,
        additional_info=city_data.additional_info,
    )

    db.add(city)

    await db.commit()
    await db.refresh(city)

    return city


async def get_cities(
    db: AsyncSession,
) -> list[City]:
    result = await db.execute(select(City))

    return list(result.scalars().all())


async def get_city(
    db: AsyncSession,
    city_id: int,
) -> City | None:
    result = await db.execute(select(City).where(City.id == city_id))

    return result.scalar_one_or_none()


async def delete_city(
    db: AsyncSession,
    city: City,
) -> None:
    await db.delete(city)
    await db.commit()


async def create_temperature(
    db: AsyncSession, city_id: int, date_time: datetime, temperature: float
) -> Temperature:
    record = Temperature(
        city_id=city_id,
        date_time=date_time,
        temperature=temperature
    )
    db.add(record)
    await db.commit()
    await db.refresh(record)
    return record


async def get_temperatures(
    db: AsyncSession, city_id: int | None = None
) -> list[Temperature] | None:
    stmt = select(Temperature)
    if city_id is not None:
        stmt = stmt.where(Temperature.city_id == city_id)
    result = await db.execute(stmt)
    return list(result.scalars().all())

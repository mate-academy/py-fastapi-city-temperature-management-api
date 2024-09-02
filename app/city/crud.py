from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.city.models import DBCity
from app.city.schemas import City, CityCreate


async def get_all_city(db: AsyncSession) -> [City]:
    result = await db.execute(select(DBCity))
    cities = result.scalars().all()
    return cities


async def get_city(city_id: int, db: AsyncSession) -> DBCity:
    find_city = select(DBCity).where(DBCity.id == city_id)
    result = await db.execute(find_city)
    city = result.scalar_one_or_none()

    if city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return city


async def get_city_by_name(db: AsyncSession, name_city: str) -> DBCity | None:
    find_city_by_name = select(DBCity).where(DBCity.city == name_city)
    result = await db.execute(find_city_by_name)
    return result.scalar_one_or_none()


async def create_city(db: AsyncSession, city: CityCreate) -> DBCity:
    new_city = DBCity(**city.dict())
    db.add(new_city)
    await db.commit()
    await db.refresh(new_city)
    return new_city


async def update_city(
    db: AsyncSession, city_id: int, new_city: str, additional_info: str
) -> DBCity:
    find_city = select(DBCity).where(DBCity.id == city_id)
    result = await db.execute(find_city)
    city = result.scalar_one_or_none()

    if city is None:
        raise HTTPException(status_code=404, detail="City not found")

    city.city = new_city
    city.additional_info = additional_info
    await db.commit()

    return city


async def delete_city(city_id: int, db: AsyncSession) -> DBCity:
    find_city = select(DBCity).where(DBCity.id == city_id)
    result = await db.execute(find_city)
    city = result.scalar_one_or_none()

    if city is None:
        raise HTTPException(status_code=404, detail="City not found")

    await db.delete(city)
    await db.commit()

    return city

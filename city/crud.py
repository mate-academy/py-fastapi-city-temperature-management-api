from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from city.models import CityModel
from city.schemas import City


async def post_city(db: AsyncSession, city: City):
    db_city = CityModel(
        name=city.name,
        additional_info=city.additional_info,
    )

    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)

    return db_city


async def get_cities(db: AsyncSession):
    queryset = select(CityModel)
    result = await db.execute(queryset)
    db_cities = result.scalars().all()
    return db_cities


async def get_city(db: AsyncSession, city_id: int):
    result = await db.execute(select(CityModel).where(CityModel.id == city_id))
    return result.scalar_one_or_none()


async def update_city(
        db: AsyncSession,
        city_id: int,
        name: str,
        additional_info: str
):
    city = await get_city(db, city_id)

    if city is None:
        raise HTTPException(status_code=404, detail="City not found")

    city.name = name
    city.additional_info = additional_info

    await db.commit()
    await db.refresh(city)
    return city


async def delete_city(db: AsyncSession, city_id: int):
    city = await get_city(db, city_id)

    if city is None:
        raise HTTPException(status_code=404, detail="City not found")

    await db.delete(city)
    await db.commit()

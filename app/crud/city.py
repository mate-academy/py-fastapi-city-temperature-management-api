from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import City
from app.schemas.city import CityCreate, CityUpdate


async def create_city(session: AsyncSession, city_in: CityCreate) -> City:
    city = City(name=city_in.name, additional_info=city_in.additional_info)
    session.add(city)
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=400, detail="City with this name already exists.")
    await session.refresh(city)
    return city


async def get_cities(session: AsyncSession) -> list[City]:
    result = await session.execute(select(City).order_by(City.id))
    return list(result.scalars().all())


async def get_city(session: AsyncSession, city_id: int) -> City | None:
    result = await session.execute(select(City).where(City.id == city_id))
    return result.scalar_one_or_none()


async def update_city(session: AsyncSession, city: City, city_in: CityUpdate) -> City:
    data = city_in.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(city, field, value)

    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=400, detail="City with this name already exists.")

    await session.refresh(city)
    return city


async def delete_city(session: AsyncSession, city: City) -> None:
    await session.delete(city)
    await session.commit()

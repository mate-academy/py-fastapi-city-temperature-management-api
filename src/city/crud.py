from sqlalchemy import Row, RowMapping
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, Any, Sequence
from src.city.schemas import CityCreate, CityUpdate
from src.city.models import City as CityModel


async def get_cities(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 10
) -> Sequence[Row[Any] | RowMapping | Any]:
    query = select(CityModel).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


async def get_city(db: AsyncSession, city_id: int) -> Optional[CityModel]:
    result = await db.execute(
        select(CityModel).filter(CityModel.id == city_id)
    )
    return result.scalars().first()


async def create_city(db: AsyncSession, city: CityCreate) -> CityModel:
    db_city = CityModel(
        name=city.name,
        additional_info=city.additional_info,
    )
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)
    return db_city


async def update_city(
    db: AsyncSession,
    city_id: int,
    city_update: CityUpdate
) -> Optional[CityModel]:
    result = await db.execute(
        select(CityModel).filter(CityModel.id == city_id)
    )
    db_city = result.scalars().first()
    if db_city:
        db_city.name = city_update.name or db_city.name
        db_city.additional_info = (
                city_update.additional_info or db_city.additional_info
        )
        await db.commit()
        await db.refresh(db_city)

    return db_city


async def delete_city(db: AsyncSession, city_id: int) -> Optional[CityModel]:
    result = await db.execute(
        select(CityModel).filter(CityModel.id == city_id)
    )
    db_city = result.scalars().first()
    if db_city:
        await db.delete(db_city)
        await db.commit()

    return db_city

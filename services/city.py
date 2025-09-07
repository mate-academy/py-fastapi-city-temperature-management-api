from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database.models import CityModel
from schemas.city import (
    CityCreateSchema,
    CityUpdateSchema,
    CityPartialUpdateSchema
)


async def get_city_by_id(city_id: int, db: AsyncSession) -> CityModel:
    """Retrieve a city by ID or raise HTTPException if not found."""
    result = await db.execute(select(CityModel).where(CityModel.id == city_id))
    city = result.scalar_one_or_none()
    if not city:
        raise HTTPException(
            status_code=404,
            detail="Object not found"
        )
    return city


async def create_city(city_schema: CityCreateSchema, db: AsyncSession) -> CityModel:
    new_city = CityModel(**city_schema.model_dump())
    db.add(new_city)
    await db.commit()
    await db.refresh(new_city)
    return new_city


async def get_cities(db: AsyncSession) -> list[CityModel]:
    result = await db.execute(select(CityModel))
    cities = result.scalars().all()
    return cities


async def get_city(city_id, db: AsyncSession) -> CityModel:
    db_city = await get_city_by_id(city_id, db)
    return db_city


async def update_city(
        city_id: int,
        city_schema: CityUpdateSchema,
        db: AsyncSession
) -> CityModel:
    db_city = await get_city_by_id(city_id, db)
    db_city.name = city_schema.name
    db_city.additional_info = city_schema.additional_info
    await db.commit()
    await db.refresh(db_city)
    return db_city


async def partial_update_city(
        city_id: int,
        city_schema: CityPartialUpdateSchema,
        db: AsyncSession
) -> CityModel:
    db_city = await get_city_by_id(city_id, db)
    update_data = city_schema.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_city, key, value)
    await db.commit()
    await db.refresh(db_city)
    return db_city


async def delete_city(
        city_id: int,
        db: AsyncSession
) -> None:
    db_city = await get_city_by_id(city_id, db)
    await db.delete(db_city)
    await db.commit()

from fastapi import HTTPException, Depends
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

import city.models
import city.schemas
from dependencies import get_db


async def get_all_cities(db: AsyncSession) -> list[city.schemas.City] | None:
    query = select(city.models.City).order_by(city.models.City.name)
    result: Result = await db.execute(query)
    cities = result.scalars().all()
    return cities if cities else []


async def get_city_by_id(city_id: int, db: AsyncSession = Depends(get_db)) -> city.schemas.City:
    db_city = await get_one_city(db=db, city_id=city_id)

    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return city.schemas.City.model_validate(db_city)


async def get_one_city(db: AsyncSession, city_id: int) -> city.schemas.City | None:
    return await db.get(city.models.City, city_id)


async def upgrade_city(
        db: AsyncSession,
        city: city.schemas.City,
        city_to_update: city.schemas.CityUpdate
) -> city.schemas.City:
    for name, value in city_to_update.model_dump().items():
        if hasattr(city, name):
            setattr(city, name, value)
    await db.commit()
    await db.refresh(city)
    return city


async def create_city(db: AsyncSession, city_data: city.schemas.CityCreate):
    existing_city_query = select(city.models.City).filter_by(name=city_data.name)
    res = await db.execute(existing_city_query)
    existing_city = res.scalars().first()

    if existing_city:
        raise HTTPException(
            status_code=400,
            detail="City with this name already exists."
        )

    new_city = city.models.City(**city_data.model_dump())  # створюємо нове місто на основі схеми
    db.add(new_city)
    await db.commit()
    await db.refresh(new_city)
    return new_city


async def delete_city_from_db(db: AsyncSession, city: city.schemas.City):
    await db.delete(city)
    await db.commit()
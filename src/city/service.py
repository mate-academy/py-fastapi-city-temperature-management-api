from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update

from src.city import models
from src.city import schemas


async def get_all_cities(db: AsyncSession):
    query = select(models.City)
    cities = await db.execute(query)

    return [city[0] for city in cities.fetchall()]


async def create_city(db: AsyncSession, city: schemas.CityCreate):
    query = insert(models.City).values(
        name=city.name,
        additional_info=city.additional_info
    )

    result = await db.execute(query)
    await db.commit()
    resp = {**city.model_dump(), "id": result.lastrowid}

    return resp


async def get_city(db: AsyncSession, city_id: int):
    query = select(models.City).filter_by(id=city_id)

    db_city = await db.execute(query)

    city = db_city.scalar()

    if city is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"City with id '{city_id}' not found"
        )

    return city


async def update_city(db: AsyncSession, city_id: int, city: schemas.CityCreate):
    city_db = await get_city(db=db, city_id=city_id)

    for field, value in city.dict(exclude_unset=True).items():
        setattr(city_db, field, value)

    await db.commit()

    await db.refresh(city_db)

    return city_db


async def delete_city(db: AsyncSession, city_id: int):
    city_db = await get_city(db=db, city_id=city_id)

    await db.delete(city_db)
    await db.commit()

    return {"message": "City deleted successfully"}

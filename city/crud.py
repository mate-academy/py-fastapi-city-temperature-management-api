from fastapi import HTTPException
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from city import models, schemas


async def create_city(db: AsyncSession, city: schemas.CityCreate):
    query = insert(models.City).values(
        name=city.name,
        additional_info=city.additional_info,
    )
    result = await db.execute(query)
    await db.commit()
    res = {**city.model_dump(), "id": result.lastrowid}
    return res


async def get_list_of_cities(db: AsyncSession):
    query = select(models.City)
    cities_list = await db.execute(query)
    return [city[0] for city in cities_list.fetchall()]


async def get_city_by_id(db: AsyncSession, city_id: int):
    query = select(models.City).where(models.City.id == city_id)
    res = await db.execute(query)
    db_city = res.scalar_one_or_none()
    return db_city


async def update_city(
        db: AsyncSession,
        city_id: int,
        additional_info: str,
):
    db_city = await get_city_by_id(db=db, city_id=city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    db_city.additional_info = additional_info
    await db.commit()
    await db.refresh(db_city)
    return db_city


async def delete_city_by_id(db: AsyncSession, city_id: int):
    city = await get_city_by_id(db=db, city_id=city_id)
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")

    await db.delete(city)
    await db.commit()
    return {"detail": "City deleted"}


from fastapi import HTTPException
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession


from . import models, schemas
from .models import DBCity


async def get_cities(db: AsyncSession) -> list:

    query = select(models.DBCity)
    cities_list = await db.execute(query)
    return [city[0] for city in cities_list.fetchall()]


async def get_city(db: AsyncSession, city_id: int) -> DBCity:
    query = select(models.DBCity).filter(models.DBCity.id == city_id)
    city = await db.execute(query)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city.scalar()


async def put_city(
        db: AsyncSession,
        city_id: int,
        update_city: schemas.CityUpdate
) -> DBCity:
    query = select(models.DBCity).filter(models.DBCity.id == city_id)
    city = await db.execute(query)
    city = city.scalar()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    for key, value in update_city.model_dump().items():
        setattr(city, key, value)

    await db.commit()
    await db.refresh(city)

    return city


async def delete_city(db: AsyncSession, city_id: int) -> DBCity:
    city = await get_city(db, city_id)
    await db.delete(city)
    await db.commit()

    return city


async def create_city(db: AsyncSession, city: schemas.CityCreate) -> dict:
    query = insert(models.DBCity).values(
        name=city.name,
        additional_info=city.additional_info
    )
    result = await db.execute(query)
    await db.commit()
    resp = {**city.model_dump(), "id": result.lastrowid}
    return resp

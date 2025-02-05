from fastapi import Depends, Query, HTTPException

from city_crud import models, schemas

from db.engine import get_db

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_cities(
    db: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
):
    result = await db.execute(select(models.City).offset(skip).limit(limit))

    db_cities = result.scalars().all()

    return db_cities


async def get_city(db: AsyncSession, city_id: int):
    result = await db.execute(select(models.City).filter_by(id=city_id))

    db_city = result.scalars().first()

    if not db_city:

        raise HTTPException(status_code=404, detail=f"City with id {city_id} not found")

    return db_city


async def create_city(db: AsyncSession, city: schemas.CityCreate):
    db_city = models.City(name=city.name, additional_info=city.additional_info)

    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)

    return db_city


async def update_city(db: AsyncSession, city_id: int, updated_city: schemas.CityCreate):
    db_city = await get_city(db=db, city_id=city_id)

    db_city.name = updated_city.name
    db_city.additional_info = updated_city.additional_info

    await db.commit()
    await db.refresh(db_city)

    return db_city


async def delete_city(db: AsyncSession, city_id: int):
    db_city = await get_city(db=db, city_id=city_id)

    await db.delete(db_city)
    await db.commit()

    return {"detail": f"City with id {city_id} has been deleted"}

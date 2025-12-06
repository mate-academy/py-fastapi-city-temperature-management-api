from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.city import models, schemas


async def get_all_cities(db:AsyncSession):
    result = await db.execute(select(models.CityModel))
    cities = result.scalars().all()
    return cities


async def create_city(db: AsyncSession, city: schemas.CityCreate):
    new_city = models.CityModel(**city.model_dump())
    db.add(new_city)
    try:
        await db.commit()
        await db.refresh(new_city)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Could not create city: {str(e)}")
    return new_city


async def get_city(db: AsyncSession, city_id: int):
    result = await db.execute(select(models.CityModel).where(models.CityModel.id == city_id))
    city = result.scalar_one_or_none()
    if city is None:
        raise HTTPException(status_code=404, detail="City with such id is not found")
    return city


async def update_city(db: AsyncSession, city_id: int, city: schemas.CityUpdate):
    result = await db.execute(select(models.CityModel).where(models.CityModel.id == city_id))
    db_city = result.scalar_one_or_none()
    if db_city is None:
        raise HTTPException(status_code=404, detail="City with such id is not found")

    if city.name is not None:
        db_city.name = city.name

    if city.additional_info is not None:
        db_city.additional_info = city.additional_info

    try:
        await db.commit()
        await db.refresh(db_city)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Could not update city: {str(e)}")
    return db_city


async def delete_city(db: AsyncSession, city_id: int):
    result = await db.execute(select(models.CityModel).where(models.CityModel.id == city_id))
    city = result.scalar_one_or_none()
    if city is None:
        raise HTTPException(status_code=404, detail="City with such id is not found")

    db.delete(city)
    try:
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Could not delete city: {str(e)}")

    return {"detail": "City deleted successfully"}

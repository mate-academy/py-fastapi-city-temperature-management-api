from fastapi import HTTPException

from sqlalchemy.orm import Session
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from weather import models, schemas
from weather.utils import exception_handler


async def get_all_cities(db: AsyncSession):
    result = await db.execute(
        select(models.City)
    )
    return result.scalars().all()


@exception_handler
async def get_city_by_id(db: AsyncSession, city_id: int):
    result = await db.execute(
        select(models.City).filter(models.City.id == city_id)
    )
    city = result.scalars().first()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    return city


@exception_handler
async def get_city_by_name(db: AsyncSession, city_name: str):
    result = await db.execute(
        select(models.City).filter(models.City.name == city_name)
    )
    city = result.scalars().first()

    return city


@exception_handler
async def create_city(db: AsyncSession, city: schemas.CityCreate):
    if await get_city_by_name(db=db, city_name=city.name):
        raise HTTPException(status_code=400, detail="City already exists")

    try:
        db_city = models.City(**city.dict())
        db.add(db_city)
        await db.commit()
        await db.refresh(db_city)
    except IntegrityError as error:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create city: {str(error)}"
        )

    return db_city


@exception_handler
async def update_city_by_city_id(
        db: AsyncSession,
        city_id: int,
        city_data: schemas.CityUpdate
):
    updated_city = await get_city_by_id(db, city_id)
    if not updated_city:
        raise HTTPException(status_code=404, detail="City not found")

    try:
        for key, value in city_data.dict().items():
            setattr(updated_city, key, value)

        await db.commit()
        await db.refresh(updated_city)
    except IntegrityError as error:
        db.rollback()
        if "UNIQUE constraint failed" in str(error):
            raise HTTPException(
                status_code=400,
                detail="A city with provided name already exists"
            )

        raise HTTPException(
            status_code=500,
            detail=f"Failed to update city: {str(error)}"
        )

    return updated_city


@exception_handler
async def delete_city(db: AsyncSession, city_id: int):
    city = await get_city_by_id(db, city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    try:
        await db.delete(city)
        await db.commit()
    except Exception as error:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete city: {str(error)}"
        )
    return {"message": "City was deleted"}

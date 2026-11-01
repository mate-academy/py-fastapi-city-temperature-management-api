from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.cities.models import City
from app.cities.schemas import CityRead, CityCreate
from app.db.database import get_db


router = APIRouter()

@router.get("", response_model=list[CityRead])
async def get_cities(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(City))
    return result.scalars().all()

@router.get("/{city_id}", response_model=CityRead)
async def get_city(
    city_id: int,
    db: AsyncSession = Depends(get_db),
):
    city = await db.get(City, city_id)

    if city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return city

@router.post("", response_model=CityRead, status_code=201)
async def create_city(
    new_city: CityCreate,
    db: AsyncSession = Depends(get_db),
):
    city = City(**new_city.model_dump())
    db.add(city)

    try:
        await db.commit()
        await db.refresh(city)
        return city
    except SQLAlchemyError:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Database operation failed",
        )

@router.put("/{city_id}", response_model=CityRead)
async def update_city(
    city_id: int,
    fields_to_update: CityCreate,
    db: AsyncSession = Depends(get_db),
):
    city = await db.get(City, city_id)

    if city is None:
        raise HTTPException(status_code=404, detail="City not found")

    for field, value in fields_to_update.model_dump().items():
        setattr(city, field, value)

    try:
        await db.commit()
        await db.refresh(city)
        return city
    except SQLAlchemyError:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Database operation failed",
        )

@router.delete("/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)):
    city = await db.get(City, city_id)

    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    try:
        await db.delete(city)
        await db.commit()
    except SQLAlchemyError:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Database operation failed",
        )

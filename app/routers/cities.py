from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db
from app.models import City
from app.schemas import CityCreate, CityResponse, CityUpdate

router = APIRouter(prefix="/cities", tags=["Cities"])



@router.post("/", response_model=CityResponse, status_code=status.HTTP_201_CREATED)
async def create_city(city_in: CityCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(City).where(City.name == city_in.name))
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"City with name '{city_in.name}' already exists.",
        )
    city = City(name=city_in.name, additional_info=city_in.additional_info)
    db.add(city)
    await db.commit()
    await db.refresh(city)
    return city


@router.get("/", response_model=List[CityResponse])
async def list_cities(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(City))
    return result.scalars().all()


@router.get("/{city_id}", response_model=CityResponse)
async def get_city(city_id: int, db: AsyncSession = Depends(get_db)):
    city = await db.get(City, city_id)
    if not city:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"City with ID {city_id} not found.",
        )
    return city


@router.put("/{city_id}", response_model=CityResponse)
async def update_city(
    city_id: int, city_in: CityUpdate, db: AsyncSession = Depends(get_db)
):
    city = await db.get(City, city_id)
    if not city:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"City with ID {city_id} not found.",
        )

    if city_in.name is not None and city_in.name != city.name:
        existing = await db.execute(select(City).where(City.name == city_in.name))
        if existing.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"City name '{city_in.name}' is already taken.",
            )
        city.name = city_in.name

    if city_in.additional_info is not None:
        city.additional_info = city_in.additional_info

    await db.commit()
    await db.refresh(city)
    return city


@router.delete("/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)):
    city = await db.get(City, city_id)
    if not city:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"City with ID {city_id} not found.",
        )
    await db.delete(city)
    await db.commit()
    return None

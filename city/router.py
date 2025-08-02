from typing import List

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert

from dependencies import get_db
from . import crud, models, schemas


router = APIRouter(
    prefix="/cities",
    tags=["Cities"]
)

@router.post("/", response_model=schemas.CityInDB, status_code=status.HTTP_201_CREATED)
async def create_city(db: AsyncSession, city_data: schemas.CityCreate) -> models.City:
    query = insert(models.City).values(
        name=city_data.name,
        additional_info=city_data.additional_info
    ).returning(models.City.id)

    result = await db.execute(query)
    city_id = result.scalar_one()
    await db.commit()

    # Окремий SELECT для отримання повноцінного об'єкта
    return await crud.get_city(db, city_id)


@router.get("/", response_model=List[schemas.CityInDB])
async def read_cities(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_cities(db)

@router.get("/{city_id}", response_model=schemas.CityInDB)
async def read_city(city_id: int, db: AsyncSession = Depends(get_db)):
    city = await crud.get_city(db, city_id)
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return city

@router.delete("/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)):
    success = await crud.delete_city(db, city_id)
    if not success:
        raise HTTPException(status_code=404, detail="City not found")
    return None
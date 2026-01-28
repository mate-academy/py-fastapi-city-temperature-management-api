from typing import List

from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from cities import crud, schemas
from database import get_db

router = APIRouter()

@router.post(
    "/",
    response_model=schemas.CityRead,
    status_code=status.HTTP_201_CREATED
)
async def create_city(city: schemas.CityCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_city(db=db, city=city)


@router.get("/", response_model=List[schemas.CityRead])
async def get_cities(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_cities(db=db)


@router.delete("/{city_id}")
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)):
    success = await crud.delete_city(db=db, city_id=city_id)
    if not success:
        raise HTTPException(status_code=404, detail="City not found")
    return {"message": "City deleted successfully."}
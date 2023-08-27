from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from . import schemas, crud


router = APIRouter()


@router.post("/cities/", response_model=schemas.City)
async def create_city(
        city: schemas.CityCreate,
        db: AsyncSession = Depends(get_db)
):
    return await crud.create_city(db, city)


@router.get("/cities/", response_model=list[schemas.City])
async def get_all_cities(
    skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)
):
    return await crud.get_all_cities(db, skip, limit)


@router.get("/cities/{city_id}/", response_model=schemas.City)
async def get_city(city_id: int, db: AsyncSession = Depends(get_db)):
    city = await crud.get_city(db, city_id)
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@router.put("/cities/{city_id}/", response_model=schemas.City)
async def update_city(
        city_id: int,
        city_update: schemas.CityCreate,
        db: AsyncSession = Depends(get_db)
):
    existing_city = await crud.get_city(db, city_id)
    if existing_city is None:
        raise HTTPException(status_code=404, detail="City not found")

    updated_city = await crud.update_city(db, existing_city, city_update)
    return updated_city


@router.delete("/cities/{city_id}/")
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)):
    city = await crud.get_city(db, city_id)
    if city:
        await crud.delete_city(db, city_id)
        return {"message": "City deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="City not found")

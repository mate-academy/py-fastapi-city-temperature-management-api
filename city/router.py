from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from dependencies import get_db

from . import crud, schemas

router = APIRouter()


@router.post("/create_city", response_model=schemas.City)
async def create_city(
        city: schemas.CityCreate,
        db: AsyncSession = Depends(get_db)
):
    return await crud.create_city(db, city)


@router.get("/cities", response_model=list[schemas.City])
async def list_cities(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_cities(db)


@router.get("/cities/{city_id}", response_model=schemas.City)
async def get_city(
        city_id: int,
        db: AsyncSession = Depends(get_db)
):
    city = await crud.get_city_by_id(db, city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@router.put("/cities/{city_id}", response_model=schemas.City)
async def update_city(
        city_id: int,
        city_update: schemas.CityCreate,
        db: AsyncSession = Depends(get_db)
):
    updated = await crud.update_city_by_id(db, city_id, city_update)
    if not updated:
        raise HTTPException(status_code=404, detail="City not found")
    return updated


@router.delete("/cities/{city_id}")
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await crud.delete_city(db, city_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="City not found")
    return {"status": "deleted", "city_id": city_id}

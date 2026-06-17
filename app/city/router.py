from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.city import schemas, crud
from dependencies import get_db

router = APIRouter()


@router.get("/", response_model=list[schemas.CityResponse])
async def get_cities(db: AsyncSession = Depends(get_db)):
    return await crud.get_cities(db)


@router.get("/{city_id}", response_model=schemas.CityResponse)
async def get_city(city_id: int, db: AsyncSession = Depends(get_db)):
    db_city = await crud.get_city_by_id(db, city_id)
    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city


@router.post("/", response_model=schemas.CityResponse, status_code=201)
async def create_city(
        city: schemas.CityCreate,
        db: AsyncSession = Depends(get_db)
):
    db_city = await crud.get_city_by_name(db, city.name)
    if db_city:
        raise HTTPException(status_code=409, detail="City already exists")
    return await crud.create_city(db, city)


@router.put("/{city_id}", response_model=schemas.CityResponse)
async def update_city(
        city_id: int,
        city: schemas.CityUpdate,
        db: AsyncSession = Depends(get_db)
):
    db_city = await crud.get_city_by_id(db, city_id)
    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")
    return await crud.update_city(db, city_id, city)


@router.delete("/{city_id}", response_model=schemas.CityResponse)
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)):
    db_city = await crud.get_city_by_id(db, city_id)
    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")
    return await crud.delete_city(db, city_id)

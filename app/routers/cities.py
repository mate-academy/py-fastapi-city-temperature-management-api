from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app import crud, schemas

router = APIRouter(prefix="/cities", tags=["cities"])


@router.post("/", response_model=schemas.CityOut)
async def create_city(
    city: schemas.CreateCity,
    db: AsyncSession = Depends(get_db),
):
    existing_city = await crud.get_city_by_name(db=db, city_name=city.name)

    if existing_city is not None:
        raise HTTPException(status_code=400, detail="City already exists")

    return await crud.create_city(db=db, city=city)


@router.get("/", response_model=list[schemas.CityOut])
async def read_cities(db: AsyncSession = Depends(get_db)):
    return await crud.get_cities(db=db)


@router.get("/{city_id}", response_model=schemas.CityOut)
async def read_one_city(city_id: int, db: AsyncSession = Depends(get_db)):
    city = await crud.get_one_city(db=db, city_id=city_id)

    if city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return city


@router.put("/{city_id}", response_model=schemas.CityOut)
async def update_city(
    city_id: int,
    city: schemas.UpdateCity,
    db: AsyncSession = Depends(get_db),
):
    updated_city = await crud.update_city(db=db, city_id=city_id, city=city)

    if updated_city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return updated_city


@router.delete("/{city_id}")
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)):
    deleted_city = await crud.delete_city(db=db, city_id=city_id)

    if deleted_city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return {"message": "City deleted successfully"}
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from city import schemas, crud
from dependencies import get_db

router = APIRouter()


@router.get("/cities/", response_model=list[schemas.CityRead])
async def read_cities(db: Annotated[AsyncSession, Depends(get_db)]):
    return await crud.get_all_cities(db=db)


@router.get("/cities/{city_id}", response_model=schemas.CityRead)
async def read_city(
        city_id: int,
        db: Annotated[AsyncSession, Depends(get_db)]
):
    city = await crud.get_city_by_id(db=db, city_id=city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@router.post("/cities/", response_model=schemas.CityRead)
async def create_city(
        db: Annotated[AsyncSession, Depends(get_db)], city: schemas.CityCreate
):
    existing_city = await crud.get_city_by_name(db=db, city_name=city.name)
    if existing_city:
        raise HTTPException(status_code=400, detail="City already exists")

    return await crud.create_city(db=db, city=city)


@router.put("/cities/{city_id}", response_model=schemas.CityRead)
async def update_city(
        db: Annotated[AsyncSession, Depends(get_db)],
        city_id: int,
        city: schemas.CityUpdate
):
    existing_city = await crud.get_city_by_id(db=db, city_id=city_id)
    if not existing_city:
        raise HTTPException(status_code=404, detail="City not found")
    return await crud.update_city(db=db, city=city, city_id=city_id)


@router.delete("/cities/{city_id}", response_model=schemas.CityRead)
async def delete_city(
        db: Annotated[AsyncSession, Depends(get_db)],
        city_id: int
):
    city = await crud.get_city_by_id(db=db, city_id=city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return await crud.delete_city(db=db, city_id=city_id)

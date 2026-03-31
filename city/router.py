from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from city import schemas, crud
from dependencies import get_db

router = APIRouter()


@router.get("/cities/", response_model=list[schemas.City])
async def read_cities(db: Annotated[AsyncSession, Depends(get_db)]):
    return await crud.get_all_cities(db=db)


@router.get("/cities/{city_id}", response_model=schemas.City)
async def read_city(city_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    db_city = await crud.get_city_by_id(db, city_id)
    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")
    return await crud.get_city_by_id(db=db, city_id=city_id)


@router.post("/cities/", response_model=schemas.City)
async def create_new_city(
    city: schemas.CityCreate, db: Annotated[AsyncSession, Depends(get_db)]
):
    db_city = await crud.get_city_by_name(db=db, city_name=city.name)
    if db_city:
        raise HTTPException(status_code=400, detail="City already exists")

    return await crud.create_city(db=db, city=city)


@router.put("/cities/{city_id}", response_model=schemas.City)
async def update_existing_city(
    city_id: int, city: schemas.CityCreate, db: Annotated[AsyncSession, Depends(get_db)]
):
    db_city = await crud.get_city_by_id(db, city_id)
    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")
    return await crud.update_city(db=db, db_city=db_city, city_update=city)


@router.delete("/cities/{city_id}")
async def delete_existing_city(
    city_id: int, db: Annotated[AsyncSession, Depends(get_db)]
):
    db_city = await crud.get_city_by_id(db, city_id)
    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")
    await crud.delete_city(db=db, db_city=db_city)
    return {"message": "City deleted successfully"}

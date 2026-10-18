from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from cities import crud, schemas

router = APIRouter()

@router.post("/cities", response_model=schemas.City)
async def create_city(
    city: schemas.CityCreate,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    return await crud.create_city(db=db, city=city)

@router.get("/cities", response_model=list[schemas.City])
async def get_cities(db: Annotated[AsyncSession, Depends(get_db)]):
    return await crud.get_cities(db=db)


@router.get("/cities/{city_id}", response_model=schemas.City)
async def get_city(city_id: int, db:  Annotated[AsyncSession, Depends(get_db)]):
    city = await crud.get_city(db=db, city_id=city_id)

    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return city

@router.put("/cities/{city_id}", response_model=schemas.City)
async def update_city(city_id: int, city_update: schemas.CityUpdate, db: Annotated[AsyncSession, Depends(get_db)]) -> schemas.City:
    city = await crud.update_city(city_id=city_id, city_update=city_update, db=db)
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return city

@router.delete("/cities/{city_id}", response_model=schemas.City)
async def delete_city(city_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    return await crud.delete_city(db=db, city_id=city_id)
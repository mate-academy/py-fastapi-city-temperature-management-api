from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db

from city import schemas, crud

router = APIRouter()

@router.get("/cities/", response_model=list[schemas.City])
async def read_cities(db: Annotated[AsyncSession, Depends(get_db)]):
    return await crud.get_all_cities(db=db)

@router.get("/cities/{city_id}/", response_model=schemas.City)
async def read_city_by_id(city_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    city = await crud.get_city_by_id(db=db, city_id=city_id)

    if city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return city

@router.post("/cities/", response_model=schemas.City)
async def create_city(city: schemas.CityCreate, db: Annotated[AsyncSession, Depends(get_db)]):
    existing_city = await crud.get_city_by_name(db=db, city_name=city.name)
    if existing_city:
        raise HTTPException(status_code=400, detail="This city already exist with this name")

    return await crud.create_city(db=db, city=city)


@router.delete("/cities/{city_id}/", response_model=schemas.City)
async def delete_city_by_id(city_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    city = await crud.delete_city(db=db, city_id=city_id)

    if city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return city

@router.put("/cities/{city_id}/", response_model=schemas.City)
async def update_city_by_id(
    city_id: int,
    city: schemas.CityUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    updated_city = await crud.update_city(
        db=db,
        city_id=city_id,
        city_in=city,
    )

    if updated_city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return updated_city
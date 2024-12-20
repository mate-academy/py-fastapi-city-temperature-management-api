from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from . import schemas, crud
from dependencies import get_db

router = APIRouter()


# Retrieve a list of all cities
@router.get("/cities/", response_model=list[schemas.CityList])
async def read_cities(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_cities(db=db)


# Get the details of a specific city by ID
@router.get("/cities/{city_id}/", response_model=schemas.CityList)
async def read_city(city_id: int, db: AsyncSession = Depends(get_db)):
    city = await crud.get_city_by_id(db=db, city_id=city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city


# Create a new city
@router.post("/cities/", response_model=schemas.CityList)
async def create_city(
        city: schemas.CityCreate,
        db: AsyncSession = Depends(get_db),
):
    db_city = await crud.get_city_by_name(db=db, name=city.name)

    if db_city:
        raise HTTPException(
            status_code=400,
            detail="Such name for City already exists"
        )

    return await crud.create_city(db=db, city=city)


# Update the details of a specific city
@router.put("/cities/{city_id}/", response_model=schemas.CityList)
async def update_city(
        city_id: int,
        city_update: schemas.CityUpdate,
        db: AsyncSession = Depends(get_db),
):
    city = await crud.get_city_by_id(db=db, city_id=city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    updated_city = await crud.update_city(
        db=db,
        city_id=city_id,
        name=city_update.name,
        additional_info=city_update.additional_info,
    )
    return updated_city


# Delete a specific city
@router.delete("/cities/{city_id}/", response_model=dict)
async def delete_city(
        city_id: int,
        db: AsyncSession = Depends(get_db),
):
    city = await crud.get_city_by_id(db=db, city_id=city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return await crud.delete_city(db=db, city_id=city_id)

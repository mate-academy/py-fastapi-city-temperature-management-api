from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db_session
from . import crud, schemas


router = APIRouter()


@router.post("/cities/", response_model=schemas.City)
async def create_city(
    city: schemas.CityCreate,
    db: AsyncSession = Depends(get_db_session),
):
    return await crud.create_city(city=city, db=db)


@router.get("/cities/", response_model=list[schemas.City])
async def get_all_cities(db: AsyncSession = Depends(get_db_session)):
    return await crud.read_cities(db=db)


@router.get("/cities/{city_id}", response_model=schemas.City)
async def get_city(
    city_id: int,
    db: AsyncSession = Depends(get_db_session),
):
    city = await crud.read_city(city_id=city_id, db=db)
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@router.put("/cities/{city_id}", response_model=schemas.City)
async def update_city(
    city_id: int,
    city_update: schemas.CityUpdate,
    db: AsyncSession = Depends(get_db_session),
):
    await crud.update_city(city_id=city_id, city_update=city_update, db=db)
    return await crud.read_city(city_id=city_id, db=db)


@router.delete("/cities/{city_id}", response_model=schemas.Message)
async def delete_city(
    city_id: int,
    db: AsyncSession = Depends(get_db_session),
):
    deleted_count = await crud.delete_city(city_id=city_id, db=db)
    if deleted_count == 0:
        raise HTTPException(status_code=404, detail="City not found")
    return {"message": "City deleted successfully"}

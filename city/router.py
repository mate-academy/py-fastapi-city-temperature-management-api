from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from city import schemas, crud


router = APIRouter()

CITY_NOT_FOUND = HTTPException(status_code=404, detail="City not found")


@router.get("/cities/", response_model=list[schemas.City])
async def read_cities(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_cities(db=db)


@router.post("/cities/", response_model=schemas.City)
async def create_city(
    city: schemas.CityCreate,
    db: AsyncSession = Depends(get_db),
):

    return await crud.create_city(db=db, city=city)


@router.get("/cities/{city_id}/", response_model=schemas.City)
async def read_single_city(
    city_id: int, db: AsyncSession = Depends(get_db)
):
    db_city = await crud.get_city(db=db, city_id=city_id)
    if db_city is None:
        raise CITY_NOT_FOUND
    return db_city


@router.put("/cities/{city_id}/", response_model=schemas.City)
async def update_city(
    city_id: int,
    city_update: schemas.CityUpdate,
    db: AsyncSession = Depends(get_db),
):
    updated_city = await crud.update_city(db, city_id, city_update)
    if updated_city is None:
        raise CITY_NOT_FOUND
    return updated_city


@router.delete("/cities/{city_id}/", response_model=schemas.City)
async def delete_city(
    city_id: int,
    db: AsyncSession = Depends(get_db),
):
    deleted_city = await crud.delete_city(db=db, city_id=city_id)
    if not deleted_city:
        raise CITY_NOT_FOUND

    return deleted_city

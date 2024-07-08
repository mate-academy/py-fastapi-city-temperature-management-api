from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from . import schemas, crud

router = APIRouter()


@router.get("/cities/", response_model=List[schemas.City])
async def read_all_cities(db: AsyncSession = Depends(get_db)) -> List[schemas.City]:
    return await crud.get_all_cities(db=db)


@router.post("/cities/", response_model=schemas.City)
async def create_city(
    city: schemas.CityCreate,
    db: AsyncSession = Depends(get_db),
) -> schemas.City:
    db_city = await crud.get_city_by_name(db=db, name=city.name)

    if db_city:
        raise HTTPException(status_code=400, detail="Such city already exists")

    return await crud.create_city(db=db, city=city)


@router.get("/cities/{city_id}/", response_model=schemas.City)
async def read_single_city(
    city_id: int, db: AsyncSession = Depends(get_db)
) -> schemas.City:
    db_city = await crud.get_city(db=db, city_id=city_id)

    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return db_city


@router.delete("/cities/{city_id}/", response_model=schemas.City)
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)) -> schemas.City:
    db_city = await crud.get_city(db=db, city_id=city_id)

    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")

    deleted_city = await crud.delete_city(db=db, city_id=city_id)

    if deleted_city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return deleted_city


@router.put("/cities/{city_id}/", response_model=schemas.City)
async def update_city(
    city_id: int, city_update: schemas.CityCreate, db: AsyncSession = Depends(get_db)
) -> schemas.City:
    updated_city = await crud.update_city(
        db=db, city_id=city_id, city_update=city_update
    )

    if updated_city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return updated_city

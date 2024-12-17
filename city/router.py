from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from city import schemas, crud
from dependencies import get_db

router = APIRouter()


@router.post("/cities/", response_model=schemas.City)
async def create_city(
    city: schemas.CityCreate,
    db: AsyncSession = Depends(get_db),
):
    db_city = await crud.get_city_by_name_additional_info(
        db=db,
        city_name=city.name,
        city_additional_info=city.additional_info
    )
    if db_city:
        raise HTTPException(
            status_code=400,
            detail="Such city with such additional info already exists"
        )

    return await crud.create_city(db=db, city=city)


@router.get("/cities/", response_model=List[schemas.City])
async def list_cities(
        skip: int = 0,
        limit: int = 10,
        db: AsyncSession = Depends(get_db)
):
    result = await crud.get_cities(db, skip=skip, limit=limit)
    return result


@router.get("/cities/{city_id}/", response_model=schemas.City)
async def read_single_city(city_id: int, db: AsyncSession = Depends(get_db)):
    db_city = await crud.get_city_by_id(db=db, city_id=city_id)

    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return db_city


@router.put("/cities/{city_id}/", response_model=schemas.City)
async def update_city(
        city_id: int,
        update_city: schemas.CityUpdate,
        db: AsyncSession = Depends(get_db)
):
    db_city = await crud.get_city_by_id(db=db, city_id=city_id)

    if db_city is None:
        raise HTTPException(
            status_code=404,
            detail=f"City with id {city_id} not found"
        )

    updated_city = await crud.update_city(db=db, city_id=city_id, city=update_city)

    return updated_city


@router.delete("/cities/{city_id}/", status_code=200)
async def delete_city(
        city_id: int,
        db: AsyncSession = Depends(get_db)
):
    db_city = await crud.get_city_by_id(db=db, city_id=city_id)

    if db_city is None:
        raise HTTPException(
            status_code=404,
            detail=f"City with id {city_id} not found"
        )

    result = await crud.delete_city(db=db, db_city=db_city)

    return result

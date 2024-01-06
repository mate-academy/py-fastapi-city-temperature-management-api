from typing import Type

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from city.models import DBCity
from dependencies import get_db
from city import crud, schemas

router = APIRouter()


@router.get("/cities/", response_model=list[schemas.City])
async def read_cities(db: AsyncSession = Depends(get_db)) -> [DBCity]:
    return await crud.get_all_cities(db=db)


@router.post("/cities/", response_model=schemas.City)
async def create_city(
    city: schemas.CityIn,
    db: AsyncSession = Depends(get_db),
) -> dict:
    return await crud.create_city(db=db, city=city)


@router.get("/cities/{city_id}/", response_model=schemas.City)
async def read_single_city(
        city_id: int,
        db: AsyncSession = Depends(get_db)
) -> Type[DBCity]:
    city = await crud.get_city(db=db, city_id=city_id)
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return city


@router.put("/cities/{city_id}/", response_model=schemas.CityIn)
async def update_city(
        city_id: int,
        city: schemas.CityIn,
        db: AsyncSession = Depends(get_db)
) -> dict:
    db_city = await crud.get_city(db=db, city_id=city_id)
    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")

    return await crud.update_city(db=db, city_id=city_id, city=city)


@router.delete("/cities/{city_id}/", response_model=schemas.City)
async def delete_city(
        city_id: int,
        db: AsyncSession = Depends(get_db)
) -> Type[DBCity]:
    city = await crud.get_city(db=db, city_id=city_id)
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")

    await crud.delete_city(db=db, city_id=city_id)

    return city

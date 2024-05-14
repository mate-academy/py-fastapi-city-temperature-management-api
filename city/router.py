from typing import Any

from fastapi import APIRouter, HTTPException

from dependencies import ComDB, ComLimitation
from . import crud, schemas

router = APIRouter()


@router.get("/cities/", response_model=list[schemas.City])
async def read_cities(
        db: ComDB,
        params_limit: ComLimitation
) -> list[schemas.City]:
    return await crud.get_all_cities(db=db, **params_limit)


@router.post("/cities/", response_model=schemas.City)
async def create_city(
        city: schemas.CityCreate,
        db: ComDB,
) -> dict[str, Any]:
    db_city = await crud.get_city_by_name(db=db, name=city.name)
    if db_city:
        raise HTTPException(status_code=400, detail="Such city already exists")
    return await crud.create_city(db=db, city=city)


@router.get("/cities/{city_id}/", response_model=schemas.CityDetail)
async def get_city(
        city_id: int,
        db: ComDB
) -> schemas.CityDetail:
    city = await crud.get_city_by_id(db=db, city_id=city_id)

    if city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return city


@router.put("/cities/{city_id}/", response_model=schemas.City)
async def update_city(
        city_id: int,
        city: schemas.CityUpdate,
        db: ComDB,
) -> schemas.CityDetail:
    city = await crud.update_city(db=db, city_id=city_id, updated_city=city)

    if city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return city


@router.delete("/cities/{city_id}/", response_model=schemas.City)
async def delete_city(
        city_id: int,
        db: ComDB
) -> schemas.CityDetail:
    city = await crud.delete_city(db=db, city_id=city_id)

    if city is None:
        raise HTTPException(status_code=404, detail="City does`t exist")
    return city

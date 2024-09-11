from typing import Any

from fastapi import APIRouter, HTTPException

from city.crud import (
    get_all_cities,
    get_city_by_id,
    get_city_by_name,
    create_city,
    update_city,
    delete_city,
)
from city.schemas import (
    City,
    CityCreate,
    CityUpdate,
    CityDetail,
)
from dependencies import CommonDB, CommonLimitation

router = APIRouter()


@router.get("/cities/", response_model=list[City])
async def read_cities_endpoint(
        db: CommonDB,
        params_limit: CommonLimitation
) -> list[City]:
    return await get_all_cities(db=db, **params_limit)


@router.post("/cities/", response_model=City)
async def create_city_endpoint(
        city: CityCreate,
        db: CommonDB,
) -> dict[str, Any]:
    db_city = await get_city_by_name(db=db, name=city.name)
    if db_city:
        raise HTTPException(status_code=400, detail="Such city already exists")
    return await create_city(db=db, city=city)


@router.get("/cities/{city_id}/", response_model=CityDetail)
async def get_city_endpoint(
        city_id: int,
        db: CommonDB
) -> CityDetail:
    city = await get_city_by_id(db=db, city_id=city_id)

    if city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return city


@router.put("/cities/{city_id}/", response_model=City)
async def update_city_endpoint(
        city_id: int,
        city: CityUpdate,
        db: CommonDB,
) -> CityDetail:
    city = await update_city(db=db, city_id=city_id, updated_city=city)

    if city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return city


@router.delete("/cities/{city_id}/", response_model=City)
async def delete_city_endpoint(
        city_id: int,
        db: CommonDB
) -> CityDetail:
    city = await delete_city(db=db, city_id=city_id)

    if city is None:
        raise HTTPException(status_code=404, detail="City does`t exist")
    return city
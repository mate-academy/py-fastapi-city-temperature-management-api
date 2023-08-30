from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from city.models import DBCity
from city.crud import (
    create_city,
    delete_city_data,
    get_cities_list,
    get_city_by_id,
    update_city_data,
)
from city.schemas import City, CityCreate
from dependencies import get_db


router = APIRouter(
    prefix="/cities",
    tags=["cities"],
)


CITY_NOT_FOUND = HTTPException(
    status_code=404,
    detail="City with provided id is not found"
)
CITY_ALREADY_EXIST = HTTPException(
    status_code=400,
    detail="City with such name already exist"
)


@router.get("/", response_model=list[City])
async def read_all_cities(db: AsyncSession = Depends(get_db)) -> List[DBCity]:
    return await get_cities_list(db=db)


@router.post("/", response_model=City)
async def create_new_city(
        city: CityCreate,
        db: AsyncSession = Depends(get_db),
) -> DBCity | dict:
    try:
        return await create_city(db=db, city=city)

    except IntegrityError:
        raise CITY_ALREADY_EXIST


@router.get("/{city_id}", response_model=City)
async def read_city_by_id(
        city_id: int,
        db: AsyncSession = Depends(get_db),
) -> DBCity:
    city = await get_city_by_id(db=db, city_id=city_id)

    if not city:
        raise CITY_NOT_FOUND

    return city


@router.put("/{city_id}", response_model=dict)
async def update_city_by_id(
        city_id: int,
        city_data: CityCreate,
        db: AsyncSession = Depends(get_db),
) -> dict:
    city = await get_city_by_id(db=db, city_id=city_id)

    if not city:
        raise CITY_NOT_FOUND

    try:
        return await update_city_data(
            db=db,
            city_id=city_id,
            city_data=city_data,
        )

    except IntegrityError:
        raise CITY_ALREADY_EXIST


@router.delete("/{city_id}", response_model=dict)
async def delete_city_by_id(
        city_id: int,
        db: AsyncSession = Depends(get_db),
) -> dict:
    city = await get_city_by_id(db=db, city_id=city_id)

    if not city:
        raise CITY_NOT_FOUND

    return await delete_city_data(db=db, city_id=city_id)

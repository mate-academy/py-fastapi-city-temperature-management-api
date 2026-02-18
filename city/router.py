from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from city.crud import (
    async_create_new_city,
    async_get_all_cities,
    async_get_one_city,
    async_update_city,
    async_delete_city
)
from city.models import City
from city.schemas import CityReadSchema, CityCreateUpdateSchema
from dependencies import async_get_db

router = APIRouter(prefix="/cities")

@router.post("/", response_model=CityReadSchema)
async def async_add_new_city(
    db: Annotated[AsyncSession, Depends(async_get_db)],
    city: CityCreateUpdateSchema
) -> City:
    return await async_create_new_city(db, city)


@router.get("/", response_model=list[CityReadSchema])
async def async_get_cities_list(
    db: Annotated[AsyncSession, Depends(async_get_db)]
) -> list[City]:
    return await async_get_all_cities(db)


@router.get("/{city_id}", response_model=CityReadSchema)
async def async_get_city_from_id(
    db: Annotated[AsyncSession, Depends(async_get_db)],
    city_id: int,
) -> City:
    return await async_get_one_city(db, city_id)


@router.put("/{city_id}", response_model=CityReadSchema)
async def async_update_city_from_id(
    db: Annotated[AsyncSession, Depends(async_get_db)],
    city_id: int,
    city: CityCreateUpdateSchema,
) -> City:
    return await async_update_city(db, city_id, city)


@router.delete("/{city_id}")
async def async_remove_city_from_id(
    db: Annotated[AsyncSession, Depends(async_get_db)],
    city_id: int
) -> dict:
    return await async_delete_city(db, city_id)

from typing import Annotated

from fastapi import APIRouter, Query, status

import crud
import schemas
from database import DbSession

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_city(db: DbSession, city: schemas.CityCreate) -> schemas.CityResponse:
    return await crud.create_city(db, city)


@router.get("/")
async def read_cities(
    db: DbSession,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
) -> list[schemas.CityResponse]:
    return await crud.get_cities(db, skip=skip, limit=limit)


@router.get("/{city_id}")
async def read_city(db: DbSession, city_id: int) -> schemas.CityResponse:
    return await crud.get_city(db, city_id)


@router.put("/{city_id}")
async def update_city(
    db: DbSession, city_id: int, city: schemas.CityUpdate
) -> schemas.CityResponse:
    return await crud.update_city(db, city_id, city)


@router.delete("/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_city(db: DbSession, city_id: int) -> None:
    return await crud.delete_city(db, city_id)

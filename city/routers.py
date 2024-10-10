from starlette import status
from dependencies import db_dependency
from fastapi import APIRouter, Path
from .schemas import CityCreate, CityRead, CityUpdate
from .crud import (
    city_create,
    get_cities,
    get_city_by_id,
    update_city_info,
    city_delete
)

city_router = APIRouter(
    prefix="/cities",
    tags=["cities"]
)


@city_router.post(
    "/create/",
    status_code=status.HTTP_201_CREATED,
    response_model=CityRead
)
async def create_city(db: db_dependency, city: CityCreate):
    return await city_create(db, city)


@city_router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[CityRead]
)
async def cities_list(db: db_dependency):
    return await get_cities(db)


@city_router.get(
    "/{city_id}/",
    status_code=status.HTTP_200_OK,
    response_model=CityRead
)
async def retrieve_city(db: db_dependency, city_id: int = Path(gt=0)):
    return await get_city_by_id(db, city_id)


@city_router.put(
    "/{city_id}/update/",
    status_code=status.HTTP_200_OK,
    response_model=CityRead
)
async def update_city(db: db_dependency, update_info: CityUpdate, city_id: int = Path(gt=0)):
    return await update_city_info(db, update_info, city_id)


@city_router.delete(
    "/{city_id}/delete/",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_city(db: db_dependency, city_id: int = Path(gt=0)):
    return await city_delete(db, city_id)

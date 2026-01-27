from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.city_app import crud
from src.city_app import City, CityCreate, CityUpdate
from src.utils import get_db

city_router = APIRouter(
    prefix="/cities",
    tags=["City"],
)


@city_router.get("/", response_model=List[City], tags=["City"])
async def get_list_of_cities(
        db: AsyncSession = Depends(get_db),
        skip: int = 0,
        limit: int = 100,
) -> List[City]:
    cities = await crud.get_list_of_city(db=db, skip=skip, limit=limit)
    return cities


@city_router.get("/{city_id}/", response_model=City, tags=["City"])
async def get_city_by_id(
        city_id: int,
        db: AsyncSession = Depends(get_db)
) -> City:
    city = await crud.get_city_by_id(db=db, city_id=city_id, )
    return city


@city_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=City,
    tags=["City"]
)
async def create_new_city(
        city: CityCreate,
        db: AsyncSession = Depends(get_db)
) -> City:
    city = await crud.create_new_city(db=db, city=city)
    return city


@city_router.put("/{city_id}/", response_model=City, tags=["City"])
async def update_city(
        city_id: int,
        city_data: CityUpdate,
        db: AsyncSession = Depends(get_db)
) -> City:
    city = await crud.update_city(db=db, city_id=city_id, city=city_data)
    return city


@city_router.delete(
    "/{city_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["City"]
)
async def delete_city(
        city_id: int,
        db: AsyncSession = Depends(get_db)
) -> None:

    await crud.delete_city(db=db, city_id=city_id)

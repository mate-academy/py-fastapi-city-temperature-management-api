from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    status
)
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_db
from .models import City
from .schemas import (
    CityReadSchema,
    CityCreateSchema,
)
from .crud import (
    create_city,
    get_all_cities,
    delete_city_by_id,
    update_city_by_id,
)

city_router = APIRouter()


@city_router.post(
    "/cities/",
    response_model=CityReadSchema,
    status_code=status.HTTP_201_CREATED
)
async def add_city(
    city_data: CityCreateSchema,
    db: Annotated[AsyncSession, Depends(get_db)]
) -> City:
    return await create_city(db=db, city_data=city_data)


@city_router.get(
    "/cities/",
    response_model=list[CityReadSchema],
    status_code=status.HTTP_200_OK
)
async def get_cities(
    db: Annotated[AsyncSession, Depends(get_db)]
) -> list[City]:
    return await get_all_cities(db=db)


@city_router.delete(
    "/cities/{city_id}/",
    response_model=list[CityReadSchema],
    status_code=status.HTTP_200_OK
)
async def delete_city(
    db: Annotated[AsyncSession, Depends(get_db)],
    city_id: int
) -> list[City]:
    return await delete_city_by_id(db=db, city_id=city_id)


@city_router.put(
    "/cities/{city_id}/",
    response_model=list[CityReadSchema],
    status_code=status.HTTP_200_OK
)
async def update_city(
    db: Annotated[AsyncSession, Depends(get_db)],
    city_id: int,
    city_data: CityCreateSchema
) -> list[City]:
    return await update_city_by_id(
        db=db,
        city_id=city_id,
        city_data=city_data
    )

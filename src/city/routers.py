from fastapi import APIRouter, Depends, status
from sqlalchemy import Row, RowMapping
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Any, Sequence, Dict

from src.city import crud
from src.dependencies import get_db, pagination_params
from src.city.schemas import City as CitySchema, CityCreate, CityUpdate
from src.exceptions import CityNotFoundError

router = APIRouter()


@router.post(
    "/cities/",
    response_model=CitySchema,
    status_code=status.HTTP_201_CREATED
)
async def create_city(
        city: CityCreate,
        db: AsyncSession = Depends(get_db)
) -> CitySchema:
    return await crud.create_city(db, city)


@router.get("/cities/", response_model=List[CitySchema])
async def get_cities(
        pagination: Dict[str, int] = Depends(pagination_params),
        db: AsyncSession = Depends(get_db)
) -> Sequence[Row[Any] | RowMapping | Any]:
    return await crud.get_cities(
        db, skip=pagination["skip"], limit=pagination["limit"]
    )


@router.get("/cities/{city_id}/", response_model=CitySchema)
async def get_city(
        city_id: int,
        db: AsyncSession = Depends(get_db)
) -> CitySchema:
    city = await crud.get_city(db, city_id)
    if city is None:
        raise CityNotFoundError()

    return city


@router.put("/cities/{city_id}/", response_model=CitySchema)
async def update_city(
        city_id: int,
        city_update: CityUpdate,
        db: AsyncSession = Depends(get_db)
) -> CitySchema:
    updated_city = await crud.update_city(db, city_id, city_update)
    if updated_city is None:
        raise CityNotFoundError()

    return updated_city


@router.delete("/cities/{city_id}/", response_model=CitySchema)
async def delete_city(
    city_id: int,
    db: AsyncSession = Depends(get_db)
) -> CitySchema:
    deleted_city = await crud.delete_city(db, city_id)
    if deleted_city is None:
        raise CityNotFoundError()

    return deleted_city

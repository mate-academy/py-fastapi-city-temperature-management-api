from typing import Sequence

from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from city import schemas, crud, models
from dependencies import get_db

router = APIRouter()


@router.get("/cities/", response_model=list[schemas.CityList])
async def get_cities_list(
        db: AsyncSession = Depends(get_db)
) -> Sequence[models.City]:
    return await crud.get_cities_list(db=db)


@router.post("/cities/", response_model=schemas.CityCreate)
async def create_city(
        city: schemas.CityCreate,
        db: AsyncSession = Depends(get_db)
) -> models.City:
    return await crud.create_city(city=city, db=db)


@router.get("/cities/{city_id}", response_model=schemas.CityList)
async def get_city(
        city_id: int,
        db: AsyncSession = Depends(get_db)
) -> models.City:
    return await crud.get_city_by_id_or_404(city_id=city_id, db=db)


@router.put("/cities/{city_id}", response_model=schemas.CityUpdate)
async def update_city(
        city_id: int,
        city_data: schemas.CityUpdate,
        db: AsyncSession = Depends(get_db)
) -> models.City:
    return await crud.update_city(db=db, city_id=city_id, city_data=city_data)


@router.delete("/cities/{city_id}")
async def delete_city(
        city_id: int,
        db: AsyncSession = Depends(get_db)
) -> Response:
    return await crud.delete_city(db=db, city_id=city_id)

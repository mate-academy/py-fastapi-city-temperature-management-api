from typing import List

from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import CommonDB, CommonLimits
from . import schemas, crud

from city.schemas import CityIn

router = APIRouter()


@router.post("cities/", response_model=schemas.City)
async def create_city(db: CommonDB, city: schemas.CityIn) -> CityIn:
    return await crud.add_city(db=db, city=city)


@router.get("/cities/", response_model=List[CityIn])
async def get_cities(db: CommonDB, limits: CommonLimits) -> List[CityIn]:
    return await crud.get_list_of_cities(db=db, limit=limits)


@router.get("/cities/{city_id}", response_model=CityIn)
async def get_the_city(db: CommonDB, city_id: int) -> CityIn:
    return await crud.get_city(db=db, city_id=city_id)


@router.put("/cities/{city_id}", response_model=CityIn)
async def update_the_city(
        db: AsyncSession,
        city_id: int,
        city: schemas.CityIn
) -> CityIn:
    return await crud.update_city(db=db, city_id=city_id, payload_city=city)


@router.patch("/cities/{city_id}", response_model=CityIn)
async def partial_update_the_city(
        db: AsyncSession,
        city_id: int,
        city: schemas.CityPatch
) -> CityIn:
    return await crud.partial_update_city(db=db, city_id=city_id, city=city)


@router.delete("/cities/{city_id}", response_model=schemas.CityIn)
async def delete_city(db: AsyncSession, city_id: int) -> schemas.CityIn:
    return await crud.delete_city(db=db, city_id=city_id)

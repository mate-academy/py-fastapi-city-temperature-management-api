from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud
from . import schemas
from dependencies import get_db

router = APIRouter()


@router.get("/cities/", response_model=list[schemas.CitySerializer])
async def cities_list(
        skip: int = 0,
        limit: int = 100,
        db: AsyncSession = Depends(get_db)
):
    return await crud.get_all_cities(db, skip=skip, limit=limit)


@router.post("/cities/", response_model=schemas.CitySerializer)
async def create_city(
        city: schemas.CityCreateSerializer,
        db: AsyncSession = Depends(get_db)
):
    return await crud.create_city(db=db, city=city)


@router.get("/cities/{city_id}", response_model=schemas.CitySerializer)
async def city_detail(city_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.get_city(db, city_id=city_id)


@router.put("/cities/{city_id}", response_model=schemas.CitySerializer)
async def update_city(
        city_id: int,
        city_data: schemas.CityBaseSerializer,
        db: AsyncSession = Depends(get_db)
):
    return await crud.update_city(db=db, city_id=city_id, city_data=city_data)


@router.delete("/cities/{city_id}")
async def delete_city(
        city_id: int,
        db: AsyncSession = Depends(get_db)
):
    return await crud.delete_city(db=db, city_id=city_id)

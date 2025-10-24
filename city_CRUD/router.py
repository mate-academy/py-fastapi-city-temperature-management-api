from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from . import crud
from fastapi import APIRouter, Depends

from city_CRUD import schemas

router = APIRouter()


@router.get("/cities/", response_model=list[schemas.City])
async def get_cities(db: AsyncSession = Depends(get_db)):
    return await crud.get_city_list(db=db)


@router.get("/cities/{city_id}/", response_model=schemas.City)
async def get_city(city_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.get_city_by_id(db=db, city_id=city_id)


@router.post("/cities/", response_model=schemas.City)
async def create_city(
        city: schemas.CityIn,
        db: AsyncSession = Depends(get_db)
):
    return await crud.create_city(db=db, city=city)


@router.put("/cities/{city_id}/", response_model=schemas.City)
async def update_city(
        city_id: int,
        city: schemas.CityIn,
        db: AsyncSession = Depends(get_db),
):
    return await crud.update_city(db=db, city_id=city_id, city=city)


@router.delete("/cities/{city_id}/", status_code=204)
async def delete_city(
        city_id: int,
        db: AsyncSession = Depends(get_db),
):
    return await crud.delete_city(db=db, city_id=city_id)

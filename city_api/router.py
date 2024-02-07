from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from . import schemas, crud

router = APIRouter()


@router.get("/cities", response_model=list[schemas.City])
async def get_cities(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_cities(db)


@router.post("/cities", response_model=schemas.City)
async def create_city(
        city: schemas.CityCreate,
        db: AsyncSession = Depends(get_db)
):
    return await crud.create_city(db, city)


@router.put("/cities/{city_id}", response_model=schemas.City)
async def update_city(
    city_id: int,
    city: schemas.CityUpdate,
    db: AsyncSession = Depends(get_db),
):
    await crud.update_city(db=db, city=city, city_id=city_id)

    updated_city = await crud.get_city_by_id(db=db, city_id=city_id)

    return updated_city


@router.delete("/cities/{city_id}")
async def delete_city(
        city_id: int,
        db: AsyncSession = Depends(get_db),
):
    return await crud.delete_city(db, city_id)

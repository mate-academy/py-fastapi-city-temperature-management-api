from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from city import crud, schemas


router = APIRouter()


@router.get("/cities/", response_model=list[schemas.City])
async def read_cities(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_cities(db)


@router.post("/cities/", response_model=schemas.City)
async def create_city(
    city: schemas.CityBase,
    db: AsyncSession = Depends(get_db),
):
    return await crud.create_city(db=db, city=city)


@router.get("/cities/{city_id}/", response_model=schemas.City)
async def read_single_city(city_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.get_single_city(db, city_id)


@router.put("/cities/{city_id}/", response_model=schemas.City)
async def update_city(
    city_id: int,
    city: schemas.CityBase,
    db: AsyncSession = Depends(get_db),
):
    return await crud.update_city(db=db, city=city, city_id=city_id)


@router.delete("/cities/{city_id}/")
async def delete_city(
    city_id: int,
    db: AsyncSession = Depends(get_db),
):
    await crud.delete_city(db=db, city_id=city_id)
    return "Successfully deleted"

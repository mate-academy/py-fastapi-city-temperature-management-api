from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from . import crud, schemas


router = APIRouter()


@router.get("/cities/", response_model=list[schemas.City])
async def get_all_city(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_city(db=db)


@router.post("/cities/", response_model=schemas.City)
async def create_city(
        city: schemas.CityCreate,
        db: AsyncSession = Depends(get_db)
):
    return await crud.create_city(db=db, city=city)


@router.get("/cities/{city_id}/", response_model=schemas.City | None)
async def get_city_by_id(
        city_id: int,
        db: AsyncSession = Depends(get_db)
):
    return await crud.get_city(db=db, city_id=city_id)


@router.put("/cities/{city_id}/", response_model=schemas.City | None)
async def update_city(
        city_id: int,
        city: schemas.CityCreate,
        db: AsyncSession = Depends(get_db)
):
    return await crud.update_city(db=db, city_id=city_id, city=city)


@router.delete("/cities/{city_id}/", response_model=schemas.City | None)
async def delete_by_id(
        city_id: int,
        db: AsyncSession = Depends(get_db)
):
    await crud.delete_city(db=db, city_id=city_id)
    return {"massage": "Everything is good!"}

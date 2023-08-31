from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from . import crud, schemas

router = APIRouter()


@router.get("/cities/", response_model=list[schemas.City])
async def get_cities(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_cities(db=db)


@router.post("/cities/", response_model=schemas.City)
async def create_city(
        city: schemas.CityBase,
        db: AsyncSession = Depends(get_db)
):
    return await crud.create_city(db=db, city=city)


@router.delete("/cities/{city_id}/")
async def delete_city(
        city_id: int,
        db: AsyncSession = Depends(get_db)
):
    return await crud.delete_city(db=db, city_id=city_id)

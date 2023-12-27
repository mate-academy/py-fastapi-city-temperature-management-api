from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from . import schemas, crud

router = APIRouter()


@router.get("/city/", response_model=list[schemas.City])
async def get_all_city(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_city(db=db)


@router.post("/city/", response_model=schemas.City)
async def create_city(
    city: schemas.CityCreate,
    db: AsyncSession = Depends(get_db),
):
    return await crud.create_city(db=db, city=city)


@router.delete("/city/{city_id}/", response_model=str)
async def delete_city_endpoint(city_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.delete_city(db=db, city_id=city_id)

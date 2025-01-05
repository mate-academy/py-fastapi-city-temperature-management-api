from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from . import schemas, crud, models
from dependencies import get_db

router = APIRouter()


# Retrieve a list of all cities
@router.get("/cities", response_model=list[schemas.City])
async def get_all_cities(db: AsyncSession = Depends(get_db)) -> models.DBCity:
    return await crud.get_city(db=db)


@router.post("/cities", response_model=schemas.City, status_code=201)
async def create_city(
        city: schemas.CityCreate,
        db: AsyncSession = Depends(get_db),
) -> models.DBCity:
    return await crud.create_city(db=db, city=city)


@router.delete("/cities/{city_id}", status_code=204)
async def delete_city(
        city_id: int,
        db: AsyncSession = Depends(get_db),
) -> None:
    await crud.delete_city(db=db, city_id=city_id)
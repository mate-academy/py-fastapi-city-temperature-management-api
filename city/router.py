from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from . import schemas, crud, models
from dependencies import get_db

router = APIRouter()


# Retrieve a list of all cities
@router.get("/cities", response_model=list[schemas.City])
async def get_all_cities(db: AsyncSession = Depends(get_db)) -> models.DBCity:
    return await crud.get_all_cities(db=db)


@router.get("/cities/{city_id}", response_model=schemas.City)
async def get_city_by_id(
        city_id: int,
        db: AsyncSession = Depends(get_db),
) -> models.DBCity:
    city = await crud.get_city_by_id(db=db, city_id=city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city


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


@router.put("/cities/{city_id}", response_model=schemas.City)
async def update_city(
        city_id: int,
        city: schemas.CityUpdate,
        db: AsyncSession = Depends(get_db),
) -> models.DBCity:
    updated_city = await crud.update_city(
        db=db,
        city_id=city_id,
        city_update_data=city,
    )
    return updated_city

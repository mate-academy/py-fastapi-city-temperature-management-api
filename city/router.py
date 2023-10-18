from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from city import schemas, crud
from dependencies import get_db

router = APIRouter()


@router.get("/cities/", response_model=list[schemas.City])
async def read_all_cities(db: AsyncSession = Depends(get_db)):
    return await crud.get_cities_list(db=db)


@router.get("/cities/{city_id}/", response_model=schemas.City)
async def read_single_city(city_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.get_single_city(city_id, db)


@router.post("/cities/", response_model=schemas.City)
async def create_city(
        city: schemas.CityCreate,
        db: AsyncSession = Depends(get_db)
):
    return await crud.create_city(db=db, city=city)


@router.put("/cities/{city_id}/", response_model=schemas.City)
async def update_city(
        city_id: int,
        new_city: schemas.CityCreate,
        db: AsyncSession = Depends(get_db),

):
    return await crud.update_city(
        city_id=city_id,
        new_city=new_city,
        db=db
    )


@router.delete("/cities/{city_id}/")
async def read_single_city(city_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.delete_city(city_id, db)

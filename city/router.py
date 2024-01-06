from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from . import schemas, crud

router = APIRouter()


@router.get("/cities/", response_model=list[schemas.City])
async def read_cities(
        db: AsyncSession = Depends(get_db)
) -> list[schemas.City]:
    return await crud.get_all_cities(db=db)


@router.get("/cities/{city_id}/", response_model=schemas.City)
async def read_city_by_id(
        city_id: int, db: AsyncSession = Depends(get_db)
) -> schemas.City:
    return await crud.get_city(db=db, city_id=city_id)


@router.post("/cities/", response_model=schemas.City)
async def add_cities(
        city: schemas.CityCreate, db: AsyncSession = Depends(get_db)
) -> schemas.City:
    return await crud.create_city(db=db, city=city)


@router.put("/cities/{city_id}/", response_model=schemas.City)
async def update_city(
    city_id: int, city: schemas.CityCreate, db: AsyncSession = Depends(get_db)
) -> schemas.City:
    return await crud.update_city(db=db, city=city, city_id=city_id)


@router.delete("/cities/{city_id}/")
async def delete_cities(
        city_id: int, db: AsyncSession = Depends(get_db)
) -> None:
    await crud.delete_city(db=db, city_id=city_id)

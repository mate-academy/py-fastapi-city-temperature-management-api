from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from . import crud, schemas

router = APIRouter()


@router.get("/cities/", response_model=list[schemas.City], status_code=200)
async def read_cities(
        db: AsyncSession = Depends(get_db)
) -> list[schemas.City]:
    return await crud.get_all_cities(db=db)


@router.post("/cities/", response_model=schemas.City, status_code=201)
async def create_city(
        city: schemas.CityCreate,
        db: AsyncSession = Depends(get_db)
) -> schemas.City:
    return await crud.create_city(db=db, city=city)


@router.get("/cities/{city_id}/", response_model=schemas.City, status_code=200)
async def read_city_by_id(
        city_id: int, db: AsyncSession = Depends(get_db)
) -> schemas.City:
    city = await crud.get_city_by_id(city_id=city_id, db=db)
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@router.put("/cities/{city_id}/", response_model=schemas.City, status_code=200)
async def update_city(
        city_id: int,
        city_update: schemas.CityCreate,
        db: AsyncSession = Depends(get_db)
) -> schemas.City:
    city = await crud.update_city(
        db=db, city_id=city_id, city_update=city_update
    )
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@router.delete("/cities/{city_id}/", status_code=204)
async def delete_city(
        city_id: int,
        db: AsyncSession = Depends(get_db)
) -> None:
    deleted_rows = await crud.delete_city(db=db, city_id=city_id)
    if deleted_rows == 0:
        raise HTTPException(status_code=404, detail="City not found")

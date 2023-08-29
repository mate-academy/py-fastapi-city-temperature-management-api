from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from city import schemas, crud


router = APIRouter()


@router.get("/cities/", response_model=list[schemas.City])
async def read_cities(db: AsyncSession = Depends(get_db), skip: int = 0, limit: int = 10):
    return await crud.get_all_cities(db=db, skip=skip, limit=limit)


@router.post("/cities/", response_model=schemas.City)
async def create_city(
    city: schemas.CityCreate,
    db: AsyncSession = Depends(get_db),
):

    return await crud.create_city(db=db, city=city)


@router.get("/cities/{city_id}/", response_model=schemas.City)
async def read_single_city(
    city_id: int, db: AsyncSession = Depends(get_db)
):
    db_city = await crud.get_city(db=db, city_id=city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city


@router.put("/cities/{city_id}/", response_model=schemas.City)
async def update_city(
    city_id: int,
    city_update: schemas.CityUpdate,
    db: AsyncSession = Depends(get_db),
):
    updated_city = await crud.update_city(db, city_id, city_update)
    if updated_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return updated_city


@router.delete("/cities/{city_id}/", response_model=schemas.City)
async def delete_city(
    city_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await crud.delete_city(db=db, city_id=city_id)

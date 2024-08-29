from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from city_app import schemas, crud

router = APIRouter()


@router.post("/cities/", response_model=schemas.City)
async def create_cities(
    city: schemas.CityCreate, db: AsyncSession = Depends(get_db)
):
    return await crud.create_city(db, city)


@router.get("/city/{city_id}/", response_model=schemas.City)
async def read_city(city_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.get_city(db, city_id)


@router.get("/cities/", response_model=list[schemas.City])
async def read_cities(db: AsyncSession = Depends(get_db)):
    return await crud.get_cities_list(db)


@router.delete("/city/{city_id}/")
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)):
    db_city = await crud.get_city(db, city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    await crud.delete_city(db, db_city)


@router.put("/city/{city_id}/")
async def particular_update_city(
    city: schemas.CityUpdate, db: AsyncSession = Depends(get_db)
):
    db_city = await crud.get_city(db, city.id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return await crud.update_city(db, db_city, city)

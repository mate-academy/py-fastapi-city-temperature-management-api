from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from cities import schemas
from cities.schemas import CityBase, CityCreate
from dependencies import get_db
import cities.crud as crud


router = APIRouter()


@router.get("/cities/", response_model=list[schemas.City])
async def read_cities_endpoint(db: AsyncSession = Depends(get_db)):
    return await crud.get_cities_list(db=db)


@router.post("/cities/", response_model=schemas.City)
async def create_city_endpoint(city: schemas.CityCreate, db: AsyncSession = Depends(get_db)):
    db_city = await crud.get_city_by_name(db=db, city_name=city.name)

    if db_city:
        raise HTTPException(status_code=400, detail="City already exists")

    return await crud.create_city(db=db, city=city)


@router.get("/cities/{city_id}/", response_model=schemas.City)
async def read_single_city_endpoint(city_id: int, db: AsyncSession = Depends(get_db)):
    db_city = await crud.get_city_by_id(db=db, city_id=city_id)

    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return db_city


@router.put("/cities/{city_id}/", response_model=schemas.City)
async def update_city_endpoint(city_id: int, city: schemas.CityUpdate, db: AsyncSession = Depends(get_db)):
    db_city = await crud.get_city_by_id(db=db, city_id=city_id)

    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return await crud.update_city(db=db, db_city=db_city, city=city)


@router.delete("/cities/{city_id}/", status_code=204)
async def delete_city_endpoint(city_id: int, db: AsyncSession = Depends(get_db)):
    db_city = await crud.get_city_by_id(db=db, city_id=city_id)

    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")

    await crud.delete_city(db=db, city=db_city)

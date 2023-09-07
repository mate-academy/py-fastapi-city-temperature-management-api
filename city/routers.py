from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from city import schemas
from city.crud import create_city, get_all_cities, get_city_by_id, delete_city
from dependencies import get_db

router = APIRouter()


@router.post("/cities/", response_model=schemas.CityCreate)
async def city_post(city: schemas.CityCreate, db: AsyncSession = Depends(get_db)):
    if await get_city_by_id(db=db, id=city.name):
        raise HTTPException(status_code=400, detail="Such city already exist")

    return await create_city(db=db, city=city)


@router.get("/cities/", response_model=list[schemas.City])
async def city_get(db: AsyncSession = Depends(get_db)):
    return await get_all_cities(db=db)


@router.get("/cities/{id}/", response_model=schemas.City)
async def city_get_by_id(id: int, db: AsyncSession = Depends(get_db)):
    return await get_city_by_id(db=db, id=id)


@router.delete("/cities/{id}/", response_model=schemas.CityDelete)
async def city_delete(id: int, db: AsyncSession = Depends(get_db)):
    city = await delete_city(db=db, id=id)
    if city:
        return city

    raise HTTPException(status_code=400, detail="There is no such city")

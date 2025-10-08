from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from city import schemas, crud
from dependencies import get_db

router = APIRouter()


@router.get("/cities/", response_model=list[schemas.CityRead])
async def get_cities(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_cities(db=db)


@router.get("/cities/{city_id}", response_model=schemas.CityRead)
async def get_city(city_id: int, db: AsyncSession = Depends(get_db)):
    city = await crud.get_city_by_id(db=db, cid=city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@router.post("/cities/", response_model=schemas.CityCreate)
async def create_city(city: schemas.CityCreate, db: AsyncSession = Depends(get_db)):
    exists = await crud.get_city_by_name(db=db, city_name=city.name)
    if exists:
        raise HTTPException(status_code=400, detail="City name already exists")
    return await crud.create_city(db=db, city=city)


@router.delete("/cities/{city_id}", status_code=204)
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)):
    city = await crud.get_city_by_id(db=db, cid=city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    await crud.delete_city(db=db, city=city)
    return None


@router.put("/cities/{city_id}", response_model=schemas.CityRead)
async def update_city(
    city_id: int, city_data: schemas.CityCreate, db: AsyncSession = Depends(get_db)
):
    return await crud.update_city(city_id=city_id, city_data=city_data, db=db)

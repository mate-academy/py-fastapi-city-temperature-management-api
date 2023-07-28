from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from city import schemas, crud
from dependencies import get_db

router = APIRouter()


@router.get("/city/", response_model=list[schemas.City])
async def read_all_cities(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_city(db=db)


@router.post("/city/", response_model=schemas.City)
async def create_new_city(city: schemas.CityCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_city(db=db, city=city)


@router.get("/city/{city_id}", response_model=schemas.City)
async def read_city_by_id(city_id: int, db: AsyncSession = Depends(get_db)):
    city = await crud.get_city_by_id(db=db, city_id=city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@router.put("/city/{city_id}", response_model=dict)
async def update_city_by_id(city_id: int, city_data: schemas.CityCreate, db: AsyncSession = Depends(get_db)):
    city = await crud.get_city_by_id(db=db, city_id=city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return await crud.update_city(db=db, city_id=city_id, city_data=city_data)


@router.delete("/city/{city_id}", response_model=dict)
async def delete_city_by_id(city_id: int, db: AsyncSession = Depends(get_db)):
    city = await crud.get_city_by_id(db=db, city_id=city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return await crud.delete_city(db=db, city_id=city_id)

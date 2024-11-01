from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from city import crud, schemas
from database import AsyncSessionLocal

router = APIRouter()


async def get_db():
    async with AsyncSessionLocal() as db:
        yield db


@router.get("/", response_model=list[schemas.City])
async def read_city(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_cities(db=db)


@router.get("/{city_id}/", response_model=schemas.City)
async def read_single_city(city_id: int, db: AsyncSession = Depends(get_db)):
    city = await crud.get_city(db=db, city_id=city_id)
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@router.post("/", response_model=schemas.CityBase)
async def create_city(city: schemas.CityBase, db: AsyncSession = Depends(get_db)):
    return await crud.create_city(city=city, db=db)


@router.delete("/{city_id}/", response_model=schemas.CityBase)
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)):
    city = await crud.delete_city(db=db, city_id=city_id)
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return city

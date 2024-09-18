from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)
from sqlalchemy.ext.asyncio import AsyncSession

from city import schemas, crud
from db.engine import get_db


router = APIRouter()


@router.get("/", response_model=list[schemas.CityList])
async def fetch_all_cities(db: AsyncSession = Depends(get_db)):
    cities = await crud.get_all_city(db)
    return cities


@router.post("/", response_model=schemas.CityList, status_code=status.HTTP_201_CREATED)
async def create_city(city: schemas.CityCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_city(db=db, city=city)


@router.get("/{city_id}", response_model=schemas.CityList)
async def fetch_city_by_id(city_id: int, db: AsyncSession = Depends(get_db)):
    db_city = await crud.get_city_by_id(db, city_id=city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail=f"City with id {city_id} not found")
    return db_city


@router.delete("/{city_id}", response_model=schemas.CityList)
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)):
    db_city = await crud.delete_city_by_id(db=db, city_id=city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city


@router.put("/{city_id}", response_model=schemas.CityList)
async def update_city(city_id: int, city: schemas.CityCreate, db: AsyncSession = Depends(get_db)):
    rowcount = await crud.update_city(db=db, city_id=city_id, city_update=city)
    if rowcount == 0:
        raise HTTPException(status_code=404, detail=f"City with id {city_id} not found")
    return await crud.get_city_by_id(db, city_id=city_id)

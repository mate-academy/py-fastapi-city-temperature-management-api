from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
import city.schemas, city.crud

router = APIRouter(
    prefix="/cities",
    tags=["Cities"]
)

@router.post("/", response_model=city.schemas.City)
async def create_city(city_data: city.schemas.CityCreate, db: AsyncSession = Depends(get_db)):
    return await city.crud.create_city(db, city_data)

@router.get("/", response_model=list[city.schemas.City])
async def read_cities(db: AsyncSession = Depends(get_db)):
    return await city.crud.get_cities(db)

@router.get("/{city_id}", response_model=city.schemas.City)
async def read_city(city_id: int, db: AsyncSession = Depends(get_db)):
    db_city = await city.crud.get_city(db, city_id)
    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city

@router.put("/{city_id}", response_model=city.schemas.City)
async def update_city(city_id: int, city: city.schemas.CityUpdate, db: AsyncSession = Depends(get_db)):
    db_city = await city.crud.update_city(db, city_id, city)
    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city

@router.delete("/{city_id}")
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)):
    db_city = await city.crud.delete_city(db, city_id)
    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")
    return {"message": "City deleted successfully"}
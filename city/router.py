from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import httpx
from database import get_db
from . import crud
from .schemas import CityCreate, City


router = APIRouter(prefix="/cities", tags=["cities"])


@router.get("/", response_model=list[City])
async def read_cities(db: AsyncSession = Depends(get_db)):
    return await crud.get_cities(db)


@router.get("/{city_id}", response_model=City)
async def read_city(city_id: int, db: AsyncSession = Depends(get_db)):
    db_city = await crud.get_city(db, city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city


@router.post("/", response_model=City)
async def create_city(city: CityCreate, db: AsyncSession = Depends(get_db)):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://wttr.in/{city.name}?format=j1")
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail=f"City '{city.name}' not found in weather API")
    return await crud.create_city(db, city)


@router.put("/{city_id}", response_model=City)
async def update_city(city_id: int, city: CityCreate, db: AsyncSession = Depends(get_db)):
    db_city = await crud.update_city(db, city_id, city)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city


@router.delete("/{city_id}", response_model=City)
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)):
    db_city = await crud.delete_city(db, city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city

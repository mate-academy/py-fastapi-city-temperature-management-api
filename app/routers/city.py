from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import AsyncSessionLocal
from app.schemas.city import CityCreate, CityOut
from app.crud import city as crud_city

router = APIRouter(prefix="/cities", tags=["Cities"])

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@router.post("/", response_model=CityOut)
async def create_city(city: CityCreate, db: AsyncSession = Depends(get_db)):
    return await crud_city.create_city(db=db, city=city)

@router.get("/", response_model=list[CityOut])
async def list_cities(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await crud_city.get_cities(db=db, skip=skip, limit=limit)

@router.get("/{city_id}", response_model=CityOut)
async def get_city(city_id: int, db: AsyncSession = Depends(get_db)):
    return await crud_city.get_city(db=db, city_id=city_id)

@router.put("/{city_id}", response_model=CityOut)
async def update_city(city_id: int, city: CityCreate, db: AsyncSession = Depends(get_db)):
    return await crud_city.update_city(db=db, city_id=city_id, city=city)

@router.delete("/{city_id}", response_model=CityOut)
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)):
    return await crud_city.delete_city(db=db, city_id=city_id)

from fastapi import APIRouter, Depends, HTTPException
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
    return await crud_city.create_city(db, city)

@router.get("/", response_model=list[CityOut])
async def get_all(db: AsyncSession = Depends(get_db)):
    return await crud_city.get_all_cities(db)

@router.delete("/{city_id}")
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)):
    city = await crud_city.delete_city(db, city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return {"detail": "City deleted"}

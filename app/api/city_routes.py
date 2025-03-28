from select import select

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models import City
from app.schemas import CityOut, CityCreate

router = APIRouter()

@router.get("/cities", response_model=list[CityOut])
async def get_cities(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(City))
    cities = result.scalars().all()
    return cities

@router.post("/cities", response_model=CityOut)
async def create_city(city: CityCreate, db: AsyncSession = Depends(get_db)):
    new_city = City(name=city.name, additional_info=city.additional_info)
    db.add(new_city)
    await db.commit()
    await db.refresh(new_city)
    return new_city
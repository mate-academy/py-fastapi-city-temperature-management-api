from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.cities.models import City
from app.cities.schemas import CityCreate, CityResponse, CityUpdate


router = APIRouter(prefix="/cities", tags=["Cities"])


@router.post("/", response_model=CityResponse, status_code=status.HTTP_201_CREATED)
async def create_city(city_data: CityCreate, db: AsyncSession = Depends(get_db)):
    query = select(City).where(City.name == city_data.name)
    result = await db.execute(query)
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="City already exists")

    new_city = City(**city_data.model_dump())
    db.add(new_city)
    await db.commit()
    await db.refresh(new_city)
    return new_city


@router.get("/", response_model=list[CityResponse])
async def get_cities(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(City))
    return result.scalars().all()


@router.get("/{city_id}", response_model=CityResponse)
async def get_city(city_id: int, db: AsyncSession = Depends(get_db)):
    city = await db.get(City, city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@router.put("/{city_id}", response_model=CityResponse)
async def update_city(city_id: int, city_data: CityUpdate, db: AsyncSession = Depends(get_db)):
    city = await db.get(City, city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    for key, value in city_data.model_dump(exclude_unset=True).items():
        setattr(city, key, value)

    await db.commit()
    await db.refresh(city)
    return city


@router.delete("/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)):
    city = await db.get(City, city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    await db.delete(city)
    await db.commit()
    return None

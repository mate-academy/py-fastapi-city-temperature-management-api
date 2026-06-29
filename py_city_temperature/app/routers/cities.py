from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models import City
from app.schemas import CityCreate, CityUpdate, CityRead

router = APIRouter(prefix="/cities", tags=["Cities"])


@router.post("/", response_model=CityRead, status_code=201)
async def create_city(payload: CityCreate, db: AsyncSession = Depends(get_db)):
    city = City(**payload.model_dump())
    db.add(city)
    await db.commit()
    await db.refresh(city)
    return city


@router.get("/", response_model=list[CityRead])
async def list_cities(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(City))
    return result.scalars().all()


@router.get("/{city_id}", response_model=CityRead)
async def get_city(city_id: int, db: AsyncSession = Depends(get_db)):
    city = await db.get(City, city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@router.put("/{city_id}", response_model=CityRead)
async def update_city(
    city_id: int, payload: CityUpdate, db: AsyncSession = Depends(get_db)
):
    city = await db.get(City, city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(city, field, value)
    await db.commit()
    await db.refresh(city)
    return city


@router.delete("/{city_id}", status_code=204)
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)):
    city = await db.get(City, city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    await db.delete(city)
    await db.commit()

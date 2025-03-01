from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound

from database import SessionLocal
from temperature.crud import get_all_temperatures, get_temperature_by_id, create_temperature
from temperature.schemas import Temperature, TemperatureCreate

router = APIRouter()


async def get_db():
    async with SessionLocal() as session:
        yield session


@router.post("/temperatures", response_model=Temperature)
async def create_temperature_endpoint(temperature: TemperatureCreate, db: AsyncSession = Depends(get_db)):
    return await create_temperature(db=db, temperature=temperature)


@router.get("/temperatures", response_model=list[Temperature])
async def get_all_temperatures_endpoint(skip: int = 0, limit: int = 10, city_id: int = None,
                                        db: AsyncSession = Depends(get_db)):
    return await get_all_temperatures(db=db, skip=skip, limit=limit, city_id=city_id)


@router.get("/temperatures/{temperature_id}", response_model=Temperature)
async def get_temperature_by_id_endpoint(temperature_id: int, db: AsyncSession = Depends(get_db)):
    try:
        return await get_temperature_by_id(db=db, temperature_id=temperature_id)
    except NoResultFound:
        raise HTTPException(status_code=404, detail=f"Temperature record with id {temperature_id} not found.")

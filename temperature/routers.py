from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from temperature import crud, schemas
from database import AsyncSessionLocal

router_temp = APIRouter()


async def get_db():
    async with AsyncSessionLocal() as db:
        yield db


@router_temp.get("/", response_model=list[schemas.Temperature])
async def read_temp(db: AsyncSession = Depends(get_db)):
    return await crud.get_temp(db=db)


@router_temp.get("/{city_id}/", response_model=schemas.Temperature)
async def read_single_temp(city_id: int, db: AsyncSession = Depends(get_db)):
    temp = await crud.get_single_temp(db=db, city_id=city_id)
    if temp is None:
        raise HTTPException(status_code=404, detail="Temperature not found")
    return temp


@router_temp.post("/update")
async def update_temperatures(db: AsyncSession = Depends(get_db)):
    cities_data = await crud.get_temperature_for_city(db)
    for city_data in cities_data:
        temp_record = schemas.TemperatureCreate(
            city_id=city_data["city_id"],
            date_time=datetime.utcnow(),
            temperature=city_data["temperature"],
        )
        await crud.create_temp(db, temp_record)
    return {"message": "Temperatures updated successfully."}

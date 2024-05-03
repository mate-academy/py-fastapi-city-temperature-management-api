from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

import dependencies
from temperature.models import TemperatureModel

router = APIRouter(prefix="/temperatures", tags=["Temperatures"])


@router.get("/", response_model=list[TemperatureModel])
async def get_all_temperatures(db: AsyncSession = Depends(dependencies.get_db)):
    query = select(TemperatureModel)
    temperatures_list = await db.execute(query)
    return [temperature[0] for temperature in temperatures_list]


@router.get("/{temperature_id}", response_model=TemperatureModel)
async def get_temperature_by_id(
        temperature_id: int,
        db: AsyncSession = Depends(dependencies.get_db),
):
    temperature = await db.execute(
        select(TemperatureModel).filter(TemperatureModel.id == temperature_id)
    )
    result = temperature.scalar_one_or_none()
    if result is None:
        raise HTTPException(status_code=404, detail="Temperature not found")
    return result


@router.post("/", response_model=TemperatureModel)
async def create_temperature_record(
        temperature: TemperatureModel,
        db: AsyncSession = Depends(dependencies.get_db),
):
    db.add(temperature)
    await db.commit()
    return temperature


@router.put("/{temperature_id}", response_model=TemperatureModel)
async def update_temperature_record(
        temperature_id: int,
        temperature: TemperatureModel,
        db: AsyncSession = Depends(dependencies.get_db),
):
    db_temperature = await db.get(TemperatureModel, temperature_id)
    if db_temperature is None:
        raise HTTPException(status_code=404, detail="Temperature not found")
    for field, value in temperature.dict(exclude_unset=True).items():
        setattr(db_temperature, field, value)
    await db.commit()
    return db_temperature


@router.delete("/{temperature_id}")
async def delete_temperature_record(
        temperature_id: int,
        db: AsyncSession = Depends(dependencies.get_db),
):
    temperature = await db.get(TemperatureModel, temperature_id)
    if temperature is None:
        raise HTTPException(status_code=404, detail="Temperature not found")
    await db.delete(temperature)
    await db.commit()
    return {"message": "Temperature deleted successfully"}
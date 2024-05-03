from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from temperature.models import TemperatureModel


async def get_all_temperatures(db: AsyncSession):
    query = select(TemperatureModel)
    temperatures_list = await db.execute(query)
    return [temperature[0] for temperature in temperatures_list]


async def get_temperature_by_id(temperature_id: int, db: AsyncSession):
    temperature = await db.execute(
        select(TemperatureModel).filter(TemperatureModel.id == temperature_id)
    )
    result = temperature.scalar_one_or_none()
    if result is None:
        raise HTTPException(status_code=404, detail="Temperature not found")
    return result


async def create_temperature_record(temperature: TemperatureModel, db: AsyncSession):
    db.add(temperature)
    await db.commit()
    return temperature


async def update_temperature_record(
    temperature_id: int, new_temperature: TemperatureModel, db: AsyncSession
):
    db_temperature = await db.get(TemperatureModel, temperature_id)
    if db_temperature is None:
        raise HTTPException(status_code=404, detail="Temperature not found")
    for field, value in new_temperature.dict(exclude_unset=True).items():
        setattr(db_temperature, field, value)
    await db.commit()
    return db_temperature


async def delete_temperature_record(temperature_id: int, db: AsyncSession):
    temperature = await db.get(TemperatureModel, temperature_id)
    if temperature is None:
        raise HTTPException(status_code=404, detail="Temperature not found")
    await db.delete(temperature)
    await db.commit()
    return {"message": "Temperature deleted successfully"}

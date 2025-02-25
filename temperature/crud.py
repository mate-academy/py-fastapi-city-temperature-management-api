from sqlalchemy.future import select

from . import models, schemas
from .models import DBTemperature


async def get_all_temperatures(db, city_id: int = None):
    query = select(DBTemperature)
    if city_id is not None:
        query = query.where(DBTemperature.city_id == city_id)
    result = await db.execute(query)
    return result.scalars().all()


async def get_temperature_by_city_id(db, city_id: int):
    result = await db.execute(
        select(models.DBTemperature).where(models.DBTemperature.city_id == city_id)
    )
    return result.scalars().first()


async def create_temperature(db, temperature: schemas.TemperatureCreate):
    db_temperature = models.DBTemperature(
        city_id=temperature.city_id,
    )
    db.add(db_temperature)
    await db.commit()
    await db.refresh(db_temperature)
    return db_temperature

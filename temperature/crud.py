from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from temperature.models import DBTemperature
from temperature.schemas import TemperatureCreate, Temperature


async def get_all_temperatures(
        db: AsyncSession, skip: int = 0, limit: int = 10, city_id: int = None
):
    """
    Retrieve a list of temperature records from the database.

    Args:
        db (AsyncSession): Database session.
        skip (int): Number of records to skip (for pagination).
        limit (int): Maximum number of records to return.
        city_id (int): If provided, filter temperature records by city ID.

    Returns:
        list[Temperature]: List of temperature records.
    """
    query = select(DBTemperature).offset(skip).limit(limit)
    if city_id:
        query = select(DBTemperature).where(DBTemperature.city_id == city_id).offset(skip).limit(limit)

    result = await db.execute(query)
    temperatures = result.scalars().all()
    return temperatures


async def get_temperature_by_id(db: AsyncSession, temperature_id: int):
    """
    Retrieve a specific temperature record by its ID.

    Args:
        db (AsyncSession): Database session.
        temperature_id (int): ID of the temperature record.

    Returns:
        Temperature: The temperature instance.
    """
    result = await db.execute(select(DBTemperature).where(DBTemperature.id == temperature_id))
    temperature = result.scalar_one_or_none()
    if not temperature:
        raise NoResultFound(f"Temperature record with id {temperature_id} does not exist.")
    return temperature

async def create_temperature(db: AsyncSession, temperature: TemperatureCreate):
    db_temperature = DBTemperature(city_id_=temperature.city_id, date_time=temperature.additional_info)
    db.add(db_temperature)
    await db.commit()
    await db.refresh(db_temperature)
    return db_temperature


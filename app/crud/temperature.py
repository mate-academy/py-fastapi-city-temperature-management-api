from datetime import datetime
from typing import List

from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from services.weather_fetcher import read_temperature_api
import schemas, models
import utils


async def construct_temperature_records(db: AsyncSession) -> List[dict]:
    """
    Construct a list of temperature records for cities from the database.
    """
    db_city_records = await db.execute(select(models.City))
    db_city_objects = [
        city_record
        for city_record
        in db_city_records.scalars().all()
    ]

    temperature_api_data = await read_temperature_api(cities=db_city_objects)

    return utils.create_city_temperature_records(
        temperature_api_data
    )


async def update_temperatures(db: AsyncSession) -> schemas.TemperatureUpdate:
    """
    Updates temperature records for cities in the database.

    This function constructs temperature records for all cities, inserts new 
    temperature records for cities not already in the database, and updates 
    existing records with the latest temperature data.
    """
    temperature_records = await construct_temperature_records(db=db)

    new_records = [
        {**temperature_record, "date_time": datetime.now()}
        for temperature_record in temperature_records
    ]

    insert_result = await utils.insert_new_temperature_records(
        db=db,
        new_records=new_records
    )
    utils.logger.info(insert_result)

    return schemas.TemperatureUpdate(
        message="Temperatures for all cities updated."
    )


async def get_all_temperatures(
    db: AsyncSession,
    city_id: int | None = None
) -> List[models.Temperature]:
    """
    Retrieves all temperature records from the database,
    including their associated city data.
    If a city_id is provided, only the temperature records for that city
    are returned.
    """
    query = (
        select(models.Temperature)
        .options(selectinload(models.Temperature.city))
    )

    if city_id is not None:
        query = query.filter(models.Temperature.city_id == city_id)

    temperature_list = await db.execute(query)

    return [
        temperature
        for temperature 
        in temperature_list.scalars().all()
    ]

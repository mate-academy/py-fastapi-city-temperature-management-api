from datetime import datetime
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from cities.crud import get_cities
from temperature import models
from temperature.service import fetch_temperature_from_api


async def get_temperatures(
        db: AsyncSession,
        city_id: Optional[int] = None
) -> List[models.Temperature]:
    """
    Retrieves all temperature records. Optionally filters by `city_id`.
    :param db: AsyncSession - The database session.
    :param city_id: Optional[int] - The ID of the city to filter temperatures.
    :return: List[models.Temperature] - A list of temperature records.
    :raises HTTPException: If no temperature records are found.
    """
    query = select(models.Temperature)

    if city_id:
        query = query.where(models.Temperature.city_id == city_id)

    result = await db.execute(query)
    temperatures = result.scalars().all()

    if not temperatures:
        raise HTTPException(
            status_code=404,
            detail="No temperature records found."
        )

    return temperatures


async def update_temperatures(db: AsyncSession) -> None:
    """
    Fetches and updates temperatures for all cities
    by querying the weather API.
    :param db: AsyncSession - The database session.
    :raises HTTPException: If no cities exist in the database,
    API request fails, or no temperatures are updated.
    """
    cities = await get_cities(db=db)

    if cities is not None:
        raise HTTPException(
            status_code=404,
            detail="No cities found in the database for temperature updates."
        )

    new_temperatures = []
    for city in cities:
        temperature_value = await fetch_temperature_from_api(city.name)

        if temperature_value is None:
            raise HTTPException(
                status_code=502,
                detail=f"Failed to fetch temperature for {city.name}."
                       " Check the API or city name."
            )

        new_temperatures.append(
            models.Temperature(
                city_id=city.id,
                date_time=datetime.now(),
                temperature=temperature_value
            )
        )

    if not new_temperatures:
        raise HTTPException(
            status_code=500,
            detail="No temperature records were added."
        )

    db.add_all(new_temperatures)
    await db.commit()

import asyncio
from datetime import datetime
from typing import Optional
import logging

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.city import City
from app.models.temperature import Temperature as TemperatureModel
from app.schemas.temperature import Temperature
from app.services.weather import get_temperature_for_city as fetch_temperature
from app.exceptions import not_found_error, bad_request_error

logger = logging.getLogger(__name__)

router = APIRouter(
    tags=["temperatures"]
)


@router.post("/update")
async def update_temperatures(
        city_id: Optional[int] = Query(None,
                                       description="City ID to update (optional, if not specified - updates all cities)"),
        db: AsyncSession = Depends(get_db)
):
    if city_id is not None:
        result = await db.execute(select(City).where(City.id == city_id))
        city = result.scalar_one_or_none()

        if not city:
            raise not_found_error("City", city_id)

        cities = [city]
    else:
        result = await db.execute(select(City))
        cities = result.scalars().all()

        if not cities:
            raise not_found_error("Cities")

    temperature_tasks = [fetch_temperature(city.name) for city in cities]
    temperature_results = await asyncio.gather(*temperature_tasks, return_exceptions=True)

    created_temperatures = []
    for city, result in zip(cities, temperature_results):
        # Handle exceptions that weren't caught by the service
        if isinstance(result, Exception):
            logger.error(f"Unexpected exception for {city.name}: {result}")
            created_temperatures.append({
                "city_id": city.id,
                "city_name": city.name,
                "temperature": None,
                "error": f"Exception: {str(result)}"
            })
            continue

        temperature = result
        if temperature is not None:  # Skip cities for which temperature could not be fetched
            db_temperature = TemperatureModel(
                city_id=city.id,
                temperature=temperature,
                date_time=datetime.utcnow()
            )
            db.add(db_temperature)
            created_temperatures.append({
                "city_id": city.id,
                "city_name": city.name,
                "temperature": temperature
            })
        else:
            # Log cities for which temperature could not be fetched
            created_temperatures.append({
                "city_id": city.id,
                "city_name": city.name,
                "temperature": None,
                "error": "Failed to fetch temperature"
            })

    # Commit database changes with error handling
    try:
        await db.commit()
    except Exception as e:
        await db.rollback()
        logger.error(f"Database commit failed: {e}")
        raise bad_request_error(f"Error saving temperatures to database: {str(e)}")

    return {
        "message": "Temperatures updated successfully",
        "updated": len([t for t in created_temperatures if t.get("temperature") is not None]),
        "failed": len([t for t in created_temperatures if t.get("temperature") is None]),
        "details": created_temperatures
    }


@router.get("/", response_model=list[Temperature])
async def get_temperatures(
        city_id: Optional[int] = Query(None, description="Filter by city ID"),
        db: AsyncSession = Depends(get_db)
):
    """
    Gets a list of all temperature records.
    Can be filtered by city_id through query parameter.
    """
    if city_id is not None:
        # Filter by city_id
        result = await db.execute(
            select(TemperatureModel).where(TemperatureModel.city_id == city_id)
        )
    else:
        # Get all records
        result = await db.execute(select(TemperatureModel))

    temperatures = result.scalars().all()
    return temperatures

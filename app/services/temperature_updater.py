import asyncio

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.temperature import crud, schemas
from app.services.geocoding import get_coordinates_by_city_name
from app.services.weather import get_current_temperature


async def fetch_and_create_temperature(db: Session, city) -> schemas.TemperatureRead:

    try:
        latitude, longitude = await get_coordinates_by_city_name(city.name)
        temperature_value = await get_current_temperature(latitude, longitude)
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing city '{city.name}': {error}",
        )

    temperature_schema = schemas.TemperatureCreate(
        temperature=temperature_value,
        city_id=city.id,
    )

    db_temperature = await asyncio.to_thread(crud.create_temperature, db=db, temperature=temperature_schema)
    return db_temperature

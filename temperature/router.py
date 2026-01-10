from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from dependencies import get_db
from city.crud import get_all_cities
from . import crud, schemas
from services.get_weather import fetch_temperature

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/temperatures/update")
async def update_temperatures(db: AsyncSession = Depends(get_db)):
    cities = await get_all_cities(db)
    if not cities:
        return {"status": "no_cities", "message": "There are no cities in the database to update"}
    
    results = []
    errors = []
    
    for city in cities:
        try:
            date_time, temp_value = await fetch_temperature(city.name)
            temp = schemas.TemperatureCreate(
                city_id=city.id,
                date_time=date_time,
                temperature=temp_value,
            )
            await crud.create_temperature(db, temp)
            results.append({"city_id": city.id, "city_name": city.name, "temperature": temp_value})

        except Exception as e:
            error_msg = f"Weather service error for the city {city.name}: {str(e)}"
            logger.error(error_msg)
            errors.append({"city_id": city.id, "city_name": city.name, "error": str(e)})

    if len(errors) == len(cities) and len(cities) > 0:
        if any(isinstance(e.get('error'), str) and 'API_KEY environment variable is not set' in e.get('error', '') for e in errors):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Weather service API key is not configured. Please check the API_KEY environment variable."
            )

    
    return {
        "status": "partial_success" if errors else "success",
        "updated_count": len(results),
        "error_count": len(errors),
        "updated_cities": results,
        "errors": errors if errors else None
    }


@router.get("/temperatures", response_model=list[schemas.Temperature])
async def list_temperatures(
        city_id: int | None = None,
        db: AsyncSession = Depends(get_db)
):
    if city_id:
        return await crud.get_temperatures_by_city(db, city_id)
    return await crud.get_all_temperatures(db)

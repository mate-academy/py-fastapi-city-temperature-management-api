from fastapi import APIRouter, Depends, HTTPException, status, Query, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import asyncio
from .. import schemas, models
from ..database import get_db
from ..services.weather_service import weather_service

router = APIRouter(prefix="/temperatures", tags=["temperatures"])


@router.post("/update", status_code=status.HTTP_202_ACCEPTED)
async def update_temperatures(
        background_tasks: BackgroundTasks,
        db: Session = Depends(get_db)
):
    """Fetch and store current temperatures for all cities"""
    # Get all cities (without temperature counts)
    cities = db.query(models.City).all()

    if not cities:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No cities found in database"
        )

    # Prepare city data for API calls
    city_data = [{"id": city.id, "name": city.name} for city in cities]

    # Fetch temperatures asynchronously
    temperature_data = await weather_service.fetch_temperatures_for_cities(city_data)

    # Store temperatures in database
    for temp_data in temperature_data:
        temperature_record = models.Temperature(
            city_id=temp_data["city_id"],
            temperature=temp_data["temperature"]
        )
        db.add(temperature_record)

    db.commit()

    return {
        "message": f"Successfully updated temperatures for {len(temperature_data)} cities",
        "updated_count": len(temperature_data)
    }


@router.get("/", response_model=List[schemas.TemperatureWithCity])
def read_temperatures(
        city_id: Optional[int] = Query(None, description="Filter by city ID"),
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=1000),
        db: Session = Depends(get_db)
):
    """Get temperature records, optionally filtered by city"""
    # Start with base query
    query = db.query(models.Temperature).join(
        models.City, models.Temperature.city_id == models.City.id
    ).with_entities(
        models.Temperature,
        models.City.name.label('city_name')
    )

    # Apply city filter if provided
    if city_id:
        query = query.filter(models.Temperature.city_id == city_id)

    # Execute query with pagination
    results = query.order_by(
        models.Temperature.date_time.desc()
    ).offset(skip).limit(limit).all()

    # Convert to response models
    temperatures_with_cities = []
    for temperature, city_name in results:
        temp_dict = schemas.Temperature.model_validate(temperature).model_dump()
        temp_dict["city_name"] = city_name
        temperatures_with_cities.append(temp_dict)

    return temperatures_with_cities

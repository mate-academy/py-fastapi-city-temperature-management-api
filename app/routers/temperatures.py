from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.database import get_db
from app import models, schemas
from app.services.temperature_service import fetch_temperature_for_city

router = APIRouter(prefix="/temperatures", tags=["temperatures"])


@router.post("/update", status_code=status.HTTP_200_OK)
async def update_temperatures(db: Session = Depends(get_db)):
    cities = db.query(models.City).all()
    
    if not cities:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No cities found in the database. Please create cities first."
        )
    
    results = {
        "updated": 0,
        "failed": 0,
        "details": []
    }
    
    for city in cities:
        temperature_value = await fetch_temperature_for_city(city.name)
        
        if temperature_value is not None:
            temperature_record = models.Temperature(
                city_id=city.id,
                temperature=temperature_value,
                date_time=datetime.utcnow()
            )
            db.add(temperature_record)
            results["updated"] += 1
            results["details"].append({
                "city_id": city.id,
                "city_name": city.name,
                "temperature": temperature_value,
                "status": "success"
            })
        else:
            results["failed"] += 1
            results["details"].append({
                "city_id": city.id,
                "city_name": city.name,
                "status": "failed",
                "error": "Could not fetch temperature"
            })
    
    db.commit()
    return results


@router.get("", response_model=List[schemas.Temperature])
async def get_temperatures(
    city_id: Optional[int] = Query(None, description="Filter by city ID"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    query = db.query(models.Temperature)
    
    if city_id is not None:
        city = db.query(models.City).filter(models.City.id == city_id).first()
        if not city:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"City with id {city_id} not found"
            )
        query = query.filter(models.Temperature.city_id == city_id)
    
    temperatures = query.order_by(models.Temperature.date_time.desc()).offset(skip).limit(limit).all()
    return temperatures


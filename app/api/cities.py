from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from .. import schemas, models
from ..database import get_db

router = APIRouter(prefix="/cities", tags=["cities"])


@router.post("/", response_model=schemas.City, status_code=status.HTTP_201_CREATED)
def create_city(
        city: schemas.CityCreate,
        db: Session = Depends(get_db)
):
    """Create a new city"""
    # Check if city already exists
    existing_city = db.query(models.City).filter(
        models.City.name == city.name
    ).first()

    if existing_city:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="City with this name already exists"
        )

    db_city = models.City(**city.model_dump())
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


@router.get("/", response_model=List[schemas.CityWithCount])
def read_cities(
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=1000),
        db: Session = Depends(get_db)
):
    """Get all cities with temperature counts in a single query"""
    # Single optimized query using LEFT JOIN and GROUP BY
    cities_with_counts = db.query(
        models.City,
        func.count(models.Temperature.id).label('temperatures_count')
    ).outerjoin(
        models.Temperature,
        models.City.id == models.Temperature.city_id
    ).group_by(
        models.City.id
    ).order_by(
        models.City.id
    ).offset(skip).limit(limit).all()

    # Convert to response models
    result = []
    for city, count in cities_with_counts:
        city_data = schemas.CityWithCount.model_validate(city)
        city_data.temperatures_count = count
        result.append(city_data)

    return result


@router.get("/{city_id}", response_model=schemas.CityWithCount)
def read_city(
        city_id: int,
        db: Session = Depends(get_db)
):
    """Get a specific city by ID with temperature count"""
    # Optimized single query for specific city
    city_with_count = db.query(
        models.City,
        func.count(models.Temperature.id).label('temperatures_count')
    ).outerjoin(
        models.Temperature,
        models.City.id == models.Temperature.city_id
    ).filter(
        models.City.id == city_id
    ).group_by(
        models.City.id
    ).first()

    if not city_with_count:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found"
        )

    city, count = city_with_count
    city_data = schemas.CityWithCount.model_validate(city)
    city_data.temperatures_count = count
    return city_data


@router.put("/{city_id}", response_model=schemas.CityWithCount)
def update_city(
        city_id: int,
        city_update: schemas.CityUpdate,
        db: Session = Depends(get_db)
):
    """Update a city"""
    # Get the city first
    city = db.query(models.City).filter(models.City.id == city_id).first()
    if not city:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found"
        )

    # Update fields
    update_data = city_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(city, field, value)

    db.commit()
    db.refresh(city)

    # Get temperature count for the updated city
    count = db.query(
        func.count(models.Temperature.id)
    ).filter(
        models.Temperature.city_id == city_id
    ).scalar()

    # Create response with count
    city_data = schemas.CityWithCount.model_validate(city)
    city_data.temperatures_count = count
    return city_data


@router.delete("/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_city(
        city_id: int,
        db: Session = Depends(get_db)
):
    """Delete a city"""
    city = db.query(models.City).filter(models.City.id == city_id).first()
    if not city:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found"
        )

    db.delete(city)
    db.commit()
    return None

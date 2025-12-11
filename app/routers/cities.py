from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/cities", tags=["cities"])


@router.post("", response_model=schemas.City, status_code=status.HTTP_201_CREATED)
async def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)):
    db_city = db.query(models.City).filter(models.City.name == city.name).first()
    if db_city:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"City with name '{city.name}' already exists"
        )
    
    db_city = models.City(**city.model_dump())
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


@router.get("", response_model=List[schemas.City])
async def get_cities(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    cities = db.query(models.City).offset(skip).limit(limit).all()
    return cities


@router.get("/{city_id}", response_model=schemas.City)
async def get_city(city_id: int, db: Session = Depends(get_db)):
    city = db.query(models.City).filter(models.City.id == city_id).first()
    if not city:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"City with id {city_id} not found"
        )
    return city


@router.put("/{city_id}", response_model=schemas.City)
async def update_city(
    city_id: int, 
    city_update: schemas.CityUpdate, 
    db: Session = Depends(get_db)
):
    db_city = db.query(models.City).filter(models.City.id == city_id).first()
    if not db_city:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"City with id {city_id} not found"
        )
    
    if city_update.name and city_update.name != db_city.name:
        existing_city = db.query(models.City).filter(models.City.name == city_update.name).first()
        if existing_city:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"City with name '{city_update.name}' already exists"
            )
    
    update_data = city_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_city, field, value)
    
    db.commit()
    db.refresh(db_city)
    return db_city


@router.delete("/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_city(city_id: int, db: Session = Depends(get_db)):
    db_city = db.query(models.City).filter(models.City.id == city_id).first()
    if not db_city:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"City with id {city_id} not found"
        )
    
    db.delete(db_city)
    db.commit()
    return None


from typing import Generator
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from .database import get_db
from . import models

def get_city(db: Session, city_id: int) -> models.City:
    """Dependency to get city by ID or raise 404"""
    city = db.query(models.City).filter(models.City.id == city_id).first()
    if not city:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found"
        )
    return city

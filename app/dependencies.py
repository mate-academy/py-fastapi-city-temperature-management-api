from fastapi import Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.repositories import CityRepository
from app.repositories import TemperatureRepository


def get_city_repository(db: Session = Depends(get_db)) -> CityRepository:
    return CityRepository(db)


def get_temperature_repository(db: Session = Depends(get_db)) -> TemperatureRepository:
    return TemperatureRepository(db)

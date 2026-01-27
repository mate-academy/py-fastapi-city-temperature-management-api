from fastapi import Depends
from sqlalchemy.orm import Session
from db import get_db
from repositories import CityRepository
from repositories import TemperatureRepository


def get_city_repository(db: Session = Depends(get_db)) -> CityRepository:
    return CityRepository(db)


def get_temperature_repository(db: Session = Depends(get_db)) -> TemperatureRepository:
    return TemperatureRepository(db)

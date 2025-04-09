from fastapi import Depends, Query
from sqlalchemy.orm import Session

from src.database import get_db
from src.temperature.models import TemperatureModel


def get_temperatures(
        city_id: int = Query(None),
        db: Session = Depends(get_db)
):
    db_query = db.query(TemperatureModel)
    if city_id:
        db_query = db_query.filter(TemperatureModel.city_id == city_id)
    return db_query.all()

from datetime import datetime

from sqlalchemy.orm import Session

from models import DBCity
from temperature_api.schemas import TemperatureCreate


def create_temperature_record(
        db: Session, city_name: str, temperature: float
) -> TemperatureCreate:
    city = db.query(DBCity).filter(DBCity.name == city_name).first()
    temperature_data = TemperatureCreate(
        city_id=city.id, date_time=datetime.utcnow(), temperature=temperature
    )
    return temperature_data

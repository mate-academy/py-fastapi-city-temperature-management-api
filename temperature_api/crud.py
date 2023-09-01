from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from models import DBCity, DBTemperature
from temperature_api.schemas import TemperatureCreate


def create_temperature_record(
        db: Session, city_name: str, temperature: float
) -> TemperatureCreate:
    city = db.query(DBCity).filter(DBCity.name == city_name).first()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    temperature_data = TemperatureCreate(
        city_id=city.id, date_time=datetime.utcnow(), temperature=temperature
    )
    return temperature_data


def update_temperatures_for_cities(db: Session, temperatures_data: list) -> List[DBTemperature]:
    db_temperatures = [DBTemperature(**data.model_dump()) for data in temperatures_data]
    db.add_all(db_temperatures)
    db.commit()

    for temp in db_temperatures:
        db.refresh(temp)
    return db_temperatures

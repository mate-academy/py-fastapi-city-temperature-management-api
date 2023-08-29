from datetime import datetime

from sqlalchemy.orm import Session

from models import DBTemperature, DBCity
from temperature_api.schemas import TemperatureCreate


# def create_temperature(db: Session, temperature: TemperatureCreate):
#     db_temperature = DBTemperature(
#         city_id=temperature.city_id,
#         date_time=temperature.date_time,
#         temperature=temperature.temperature
#     )
#     db.add(db_temperature)
#     db.commit()
#     db.refresh(db_temperature)
#     return db_temperature
#
#
# def get_temperatures(db: Session, city_id: int = None):
#     query = db.query(DBTemperature)
#     if city_id:
#         query = query.filter(DBTemperature.city_id == city_id)
#     return query.all()


def create_temperature_record(
    db: Session, city_name: str, temperature: float
) -> TemperatureCreate:
    city = db.query(DBCity).filter(DBCity.name == city_name).first()
    temperature_data = TemperatureCreate(
        city_id=city.id, date_time=datetime.utcnow(), temperature=temperature
    )
    return temperature_data

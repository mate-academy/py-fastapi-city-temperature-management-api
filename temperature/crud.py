from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from temperature.models import DBTemperature


def get_temperatures(db: Session, city_id: int = None, skip: int = 0, limit: int = 10):
    query = select(DBTemperature).options(
        selectinload(DBTemperature.city)
    )
    if city_id:
        query = query.where(DBTemperature.city_id == city_id)

    temperatures = db.execute(query)
    return [temperature[0] for temperature in temperatures.fetchall()]


def update_temperatures_from_api(db: Session, city_id: int, temperature: float):
    db_temperature = DBTemperature(city_id=city_id, temperature=temperature)
    db.add(db_temperature)
    db.commit()
    db.refresh(db_temperature)

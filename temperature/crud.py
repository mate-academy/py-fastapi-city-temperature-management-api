from sqlalchemy import select
from sqlalchemy.orm import Session

from temperature import schemas
from models.temperature import DBTemperature


def get_all_temps(db: Session):
    return db.scalars(select(DBTemperature)).all()


def get_temps_by_city(db: Session, city_id: int):
    db_temps = db.scalars(
        select(DBTemperature).where(DBTemperature.city_id == city_id)
    ).all()
    return db_temps


def create_temperature(db: Session, city_id: int, temp: float | int):
    db_temperature = DBTemperature(
        city_id=city_id,
        temperature=temp,
    )
    db.add(db_temperature)
    db.commit()
    db.refresh(db_temperature)
    return db_temperature

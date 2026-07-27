
from sqlalchemy.orm import Session
from temperature_api import temp_models

import datetime



def create_temperature(
        db: Session,
        city_id: int,
        date_time: datetime,
        temperature: float
):
    new_value = temp_models.DBTemperature(
        city_id=city_id,
        date_time=date_time,
        temperature=temperature
    )
    db.add(new_value)
    db.commit()
    db.refresh(new_value)
    return new_value


def get_temperatures_list(
        db: Session
):
    return db.query(temp_models.DBTemperature).all()


def get_temperatures_by_city_id(
        db: Session,
        city_id: int
):
    return db.query(temp_models.DBTemperature).filter(temp_models.DBTemperature.city_id==city_id)
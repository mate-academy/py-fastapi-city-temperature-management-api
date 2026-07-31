from sqlalchemy import select
from sqlalchemy.orm import Session
from temperature import models


def get_all_temperature(db: Session, city_id: int | None):
    queryset = select(models.DBTemperature)
    if city_id is not None:
        queryset = queryset.where(models.DBTemperature.city_id == city_id)

    return db.scalars(queryset).all()


def create_temperature_list(db: Session, temperatures_data: list[dict]):
    temperature_list = []
    for item in temperatures_data:
        temperature_list.append(models.DBTemperature(**item))
    db.add_all(temperature_list)
    db.commit()
    return temperature_list

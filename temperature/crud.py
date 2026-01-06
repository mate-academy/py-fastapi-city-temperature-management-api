from typing import Optional, List

from sqlalchemy.orm import Session

from temperature.models import Temperature
from temperature.schemas import TemperatureUpdate, TemperatureCreate


def get_temperatures(db: Session,
                     skip: int = 0,
                     limit: int = 10) -> List[Temperature]:
    return db.query(Temperature).offset(skip).limit(limit).all()


def get_temperature_by_city(
    db: Session, city_id: int, skip: int = 0, limit: int = 10
) -> List[Temperature]:
    return db.query(Temperature).filter(Temperature.city_id == city_id).offset(skip).limit(limit).all()


def get_temperature(db: Session, temperature_id: int) -> Optional[Temperature]:
    return db.get(Temperature, temperature_id)


def create_temperature(db: Session, temp_in: TemperatureCreate) -> Temperature:
    db_temp = Temperature(**temp_in.model_dump())
    db.add(db_temp)
    db.commit()
    db.refresh(db_temp)
    return db_temp


def update_temperature(
    db: Session, temperature_id: int, temp_in: TemperatureUpdate
) -> Optional[Temperature]:
    db_temp = db.get(Temperature, temperature_id)
    if not db_temp:
        return None

    update_data = temp_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_temp, key, value)

    db.add(db_temp)
    db.commit()
    db.refresh(db_temp)
    return db_temp


def delete_temperature(db: Session, temperature_id: int) -> bool:
    db_temp = db.get(Temperature, temperature_id)
    if not db_temp:
        return False
    db.delete(db_temp)
    db.commit()
    return True

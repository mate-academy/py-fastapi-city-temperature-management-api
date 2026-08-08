from sqlalchemy.orm import Session

from temperature_api import models, schemas


def get_all_temperatures(db: Session):
    statement = db.query(models.Temperature)
    return list(db.scalars(statement).all())


def get_temperature_for_city(db: Session, city_id: int):
    statement = db.query(models.Temperature).filter(models.Temperature.city_id == city_id)
    return list(db.scalars(statement).all())


def create_temperature(
    db: Session,
    city_id: int,
    temperature_value: float,
) -> models.Temperature:
    
    db_temperature = models.Temperature(
        city_id=city_id,
        temperature=temperature_value,
    )

    db.add(db_temperature)
    db.commit()
    db.refresh(db_temperature)

    return db_temperature

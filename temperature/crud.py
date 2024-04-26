from sqlalchemy.orm import Session

from temperature import models


def get_temperatures(
        db: Session,
        skip: int = 0,
        limit: int = 10,
        city_id: int | None = None
) -> list[models.Temperature]:
    temperature = (db.query(models.Temperature)
                   .offset(skip).limit(limit).all())

    if city_id:
        temperature = temperature.filter(
            models.Temperature.city_id == city_id
        )

    return temperature


def update_temperature(db: Session, city_id: int, temperature: float):
    db_temperature = (
        db.query(models.Temperature)
        .filter(models.Temperature.city_id == city_id)
        .first()
    )
    if db_temperature:
        db_temperature.temperature = temperature
        db.commit()
        db.refresh(db_temperature)
        return db_temperature

from sqlalchemy.orm import Session

from app.temperatures import models


def get_temperatures(
        db: Session,
        city_id: int | None = None
) -> list[models.DBTemperature]:
    query = db.query(models.DBTemperature)
    if city_id is not None:
        query = query.filter(models.DBTemperature.city_id == city_id)
    return query.all()


def create_temperature(
        db: Session,
        city_id: int,
        temperature: float
) -> models.DBTemperature:
    db_temperature = models.DBTemperature(
        city_id=city_id, temperature=temperature
    )
    db.add(db_temperature)
    db.commit()
    db.refresh(db_temperature)
    return db_temperature

from sqlalchemy.orm import Session
from app.models.models import Temperature
from app.schemas.schemas import TemperatureBase


def create_temperature(db: Session, temp_data: TemperatureBase) -> Temperature:
    """Persist a new temperature record and return the ORM object."""
    db_temp = Temperature(
        city_id=temp_data.city_id,
        date_time=temp_data.date_time,
        temperature=temp_data.temperature,
    )
    db.add(db_temp)
    db.commit()
    db.refresh(db_temp)
    return db_temp


def get_temperatures(
    db: Session,
    city_id: int | None = None,
    skip: int = 0,
    limit: int = 500,
) -> list[Temperature]:
    """
    Return temperature records, optionally filtered by city_id.
    Results are ordered newest-first.
    """
    query = db.query(Temperature)
    if city_id is not None:
        query = query.filter(Temperature.city_id == city_id)
    return query.order_by(Temperature.date_time.desc()).offset(skip).limit(limit).all()
from sqlalchemy.orm import Session

from temperature import models, schemas
from temperature.models import Temperature


def get_all_temperatures(
        db: Session,
        city_id: int | None,
        skip: int = 0,
        limit: int = 10
) -> list[Temperature]:
    queryset = db.query(models.Temperature)

    if city_id is not None:
        queryset = queryset.filter(
            models.Temperature.city_id == city_id
        )

    return queryset.offset(skip).limit(limit).all()


def create_temperature(
        db: Session,
        temperature: schemas.TemperatureCreate
) -> Temperature:
    db_temperature = models.Temperature(
        city_id=temperature.city_id,
        temperature=temperature.temperature
    )
    db.add(db_temperature)
    db.commit()
    db.refresh(db_temperature)
    return db_temperature

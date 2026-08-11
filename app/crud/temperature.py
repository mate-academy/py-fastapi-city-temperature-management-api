from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Temperature
from app.schemas.temperature import TemperatureCreate


def get_temperatures(
    db: Session,
    city_id: int | None = None,
) -> list[Temperature]:
    statement = select(Temperature)

    if city_id is not None:
        statement = statement.where(Temperature.city_id == city_id)

    return list(db.scalars(statement))


def create_temperature(
        database: Session,
        temperature: TemperatureCreate,
        city_id: int
):
    database_temperature = Temperature(
        city_id=city_id,
        date_time=temperature.date_time,
        temperature=temperature.temperature,
    )
    database.add(database_temperature)
    database.commit()
    database.refresh(database_temperature)

    return database_temperature

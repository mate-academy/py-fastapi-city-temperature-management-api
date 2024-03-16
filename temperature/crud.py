from sqlalchemy.orm import Session

from temperature import schemas
from temperature.models import Temperature


def get_all_temperatures(db: Session) -> list[Temperature]:
    return db.query(Temperature).all()


def create_temperature(
        db: Session,
        temperature: schemas.TemperatureCreate
) -> Temperature:
    db_temperature = Temperature(
        city_id=temperature.city_id,
        date_time=temperature.date_time,
        temperature=temperature.temperature
    )
    db.add(db_temperature)
    db.commit()
    db.refresh(db_temperature)

    return db_temperature


def get_temperature_by_city_id(
        db: Session,
        city_id: int
) -> Temperature:
    return db.query(Temperature).filter(
            Temperature.city_id == city_id
        ).first()


def update_temperature_by_id(
        db: Session,
        temperature: schemas.TemperatureCreate,
        temperature_id: int
) -> dict[str, str]:
    db.query(Temperature).filter(
        Temperature.id == temperature_id
    ).update(
        {
            "city_id": temperature.city_id,
            "temperature": temperature.temperature,
            "date_time": temperature.date_time
        }
    )
    db.commit()
    return {"message": "Temperature updated successfully!"}

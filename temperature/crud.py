from sqlalchemy.orm import Session

from temperature import models, schemas


def get_all_temperatures(db: Session) -> list[models.Temperature]:
    return db.query(models.Temperature).all()


def create_temperature(
        db: Session,
        temperature: schemas.TemperatureCreate
) -> models.Temperature:
    db_temperature = models.Temperature(
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
) -> models.Temperature:
    return db.query(models.Temperature).filter(
            models.Temperature.city_id == city_id
        ).first()


def update_temperature_by_id(
        db: Session,
        temperature: schemas.TemperatureCreate,
        temperature_id: int
) -> dict[str, str]:
    db.query(models.Temperature).filter(
        models.Temperature.id == temperature_id
    ).update(
        {
            "city_id": temperature.city_id,
            "temperature": temperature.temperature,
            "date_time": temperature.date_time
        }
    )
    db.commit()
    return {"message": "Temperature updated successfully!"}

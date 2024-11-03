from sqlalchemy.orm import Session

from temperature import models, schemas


def create_temperature(
    db: Session, temperature: schemas.TemperatureCreateUpdate
) -> models.Temperature:
    db_temperature = models.Temperature(**temperature.model_dump())
    db.add(db_temperature)
    db.commit()
    db.refresh(db_temperature)

    return db_temperature


def get_temperature(db: Session, temperature_id: int) -> models.Temperature:
    return (
        db.query(models.Temperature)
        .filter(models.Temperature.id == temperature_id).first()
    )


def get_temperature_list(
    db: Session, city_id: int = None, skip: int = 0, limit: int = 10
) -> list[models.Temperature]:
    query = db.query(models.Temperature)

    if city_id:
        query = query.filter(models.Temperature.city_id == city_id)

    return query.offset(skip).limit(limit).all()


def update_temperature(
    db: Session,
    temperature_id: int,
    temperature: schemas.TemperatureCreateUpdate
) -> models.Temperature:
    db_temperature = (
        db.query(models.Temperature)
        .filter(models.Temperature.id == temperature_id).first()
    )

    if db_temperature:
        for key, value in temperature.model_dump().items():
            setattr(db_temperature, key, value)
        db.commit()
        db.refresh(db_temperature)

    return db_temperature


def delete_temperature(db: Session, temperature_id: int) -> bool:
    db_temperature = (
        db.query(models.Temperature)
        .filter(models.Temperature.id == temperature_id).first()
    )

    if db_temperature:
        db.delete(db_temperature)
        db.commit()
        return True

    return False

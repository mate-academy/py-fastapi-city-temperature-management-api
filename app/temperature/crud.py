from sqlalchemy.orm import Session

from app.temperature import models, schemas


def create_temperature(db: Session, temperature: schemas.TemperatureCreate):
    db_temperature = models.Temperature(**temperature.model_dump())
    db.add(db_temperature)
    db.commit()
    db.refresh(db_temperature)
    return db_temperature


def create_temperatures(db: Session, temperatures: list[schemas.TemperatureCreate]):
    db_temperatures = [models.Temperature(**t.model_dump()) for t in temperatures]
    db.add_all(db_temperatures)
    db.commit()
    for db_temperature in db_temperatures:
        db.refresh(db_temperature)
    return db_temperatures


def get_temperatures(
    db: Session,
    city_id: int | None = None,
    skip: int = 0,
    limit: int = 100,
):
    query = db.query(models.Temperature)
    if city_id is not None:
        query = query.filter(models.Temperature.city_id == city_id)
    return (
        query.order_by(models.Temperature.date_time.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

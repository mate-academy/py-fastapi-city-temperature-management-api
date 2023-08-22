from datetime import datetime

from sqlalchemy.orm import Session

from weather import schemas, models


def create_city(db: Session, city: schemas.CityCreate) -> models.City:
    db_city = models.City(**city.model_dump())
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def get_all_cities(db: Session) -> list[models.City]:
    return db.query(models.City).all()


def get_city_by_id(db: Session, city_id: int) -> models.City | None:
    return db.query(models.City).filter(models.City.id == city_id).first()


def get_city_by_name(db: Session, city_name: str) -> models.City | None:
    return db.query(models.City).filter(models.City.name == city_name).first()


def update_city(
    db: Session, city_id: int, city: schemas.CityCreate
) -> models.City | None:
    db_city = db.query(models.City).filter(models.City.id == city_id).first()

    if db_city:
        for key, value in city.model_dump().items():
            setattr(db_city, key, value)
        db.commit()
        db.refresh(db_city)
        return db_city


def delete_city(db: Session, city_id: int) -> dict:
    db.query(models.City).filter(models.City.id == city_id).delete()
    db.commit()
    return {"message": "City deleted successfully."}


def create_temperature(
    db: Session, city_id: int, date_time: datetime, temperature: float
) -> models.Temperature:
    db_temperature = models.Temperature(
        city_id=city_id, date_time=date_time, temperature=temperature
    )
    db.add(db_temperature)
    db.commit()
    db.refresh(db_temperature)
    return db_temperature


def get_all_temperatures(db: Session) -> list[models.Temperature]:
    return db.query(models.Temperature).all()


def get_temperature_by_city_id(db: Session, city_id: int) -> models.Temperature | None:
    return (
        db.query(models.Temperature)
        .filter(models.Temperature.city_id == city_id)
        .first()
    )

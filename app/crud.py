from datetime import datetime

from sqlalchemy.orm import Session

from app import models, schemas


def create_city(
    db: Session,
    city: schemas.CityCreate,
) -> models.City:
    db_city = models.City(
        name=city.name,
        additional_info=city.additional_info,
        latitude=city.latitude,
        longitude=city.longitude,
    )

    db.add(db_city)
    db.commit()
    db.refresh(db_city)

    return db_city


def get_cities(db: Session) -> list[models.City]:
    return db.query(models.City).all()


def get_city(
    db: Session,
    city_id: int,
) -> models.City | None:
    return (
        db.query(models.City)
        .filter(models.City.id == city_id)
        .first()
    )


def update_city(
    db: Session,
    city_id: int,
    city: schemas.CityCreate,
) -> models.City | None:
    db_city = get_city(db, city_id)

    if db_city is None:
        return None

    db_city.name = city.name
    db_city.additional_info = city.additional_info
    db_city.latitude = city.latitude
    db_city.longitude = city.longitude

    db.commit()
    db.refresh(db_city)

    return db_city


def delete_city(
    db: Session,
    city_id: int,
) -> models.City | None:
    db_city = get_city(db, city_id)

    if db_city is None:
        return None

    db.delete(db_city)
    db.commit()

    return db_city


def create_temperature(
    db: Session,
    city_id: int,
    temperature: float,
    date_time: datetime,
) -> models.Temperature:
    db_temperature = models.Temperature(
        city_id=city_id,
        temperature=temperature,
        date_time=date_time,
    )

    db.add(db_temperature)
    db.commit()
    db.refresh(db_temperature)

    return db_temperature


def get_temperatures(
    db: Session,
    city_id: int | None = None,
) -> list[models.Temperature]:
    query = db.query(models.Temperature)

    if city_id is not None:
        query = query.filter(
            models.Temperature.city_id == city_id
        )

    return query.all()

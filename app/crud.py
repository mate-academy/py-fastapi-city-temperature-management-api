from datetime import datetime

from sqlalchemy.orm import Session

from app import models, schemas


def create_city(db: Session, city: schemas.CityCreate):
    db_city = models.City(
        name=city.name,
        additional_info=city.additional_info
    )

    db.add(db_city)
    db.commit()
    db.refresh(db_city)

    return db_city


def get_cities(db: Session):
    return db.query(models.City).all()


def get_city(db: Session, city_id: int):
    return db.query(models.City).filter(
        models.City.id == city_id
    ).first()


def delete_city(db: Session, city_id: int):
    city = get_city(db, city_id)

    if city is None:
        return None

    db.delete(city)
    db.commit()

    return city


def create_temperature(
    db: Session,
    city_id: int,
    temperature: float,
):
    db_temperature = models.Temperature(
        city_id=city_id,
        temperature=temperature,
        date_time=datetime.utcnow(),
    )

    db.add(db_temperature)
    db.commit()
    db.refresh(db_temperature)

    return db_temperature


def get_temperatures(
    db: Session,
    city_id: int | None = None,
):
    query = db.query(models.Temperature)

    if city_id is not None:
        query = query.filter(
            models.Temperature.city_id == city_id
        )

    return query.all()

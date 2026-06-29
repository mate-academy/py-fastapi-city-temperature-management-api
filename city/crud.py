from sqlalchemy import select
from sqlalchemy.orm import Session
from city import models, schemas


def get_all_cities(db: Session):
    return db.scalars(select(models.DBCity)).all()


def get_all_cities_names(db: Session):
    return db.scalars(select(models.DBCity.name)).all()


def get_city_by_id(db: Session, city_id: int):
    return (
        db.scalars(
            select(models.DBCity)
            .where(models.DBCity.id == city_id)
        ).first()
    )


def create_city(db: Session, city: schemas.CityCreate):
    db_city = models.DBCity(
        name=city.name,
        additional_info=city.additional_info,
    )

    db.add(db_city)
    db.commit()
    db.refresh(db_city)

    return db_city


def update_city(db: Session, city_id: int, city: schemas.CityUpdate):
    db_city = get_city_by_id(db, city_id)

    if db_city is None:
        return None

    db_city.name = city.name
    db_city.additional_info = city.additional_info

    db.commit()
    db.refresh(db_city)

    return db_city


def delete_city(db: Session, city_id: int):
    db_city = get_city_by_id(db, city_id)

    db.delete(db_city)
    db.commit()

    return db_city


def get_all_temperature(db: Session, city_id: int | None = None):
    queryset = select(models.DBTemperature)

    if city_id is not None:
        queryset = queryset.where(models.DBTemperature.city_id == city_id)

    return db.scalars(queryset).all()


def create_temperature(db: Session, city_id: int, temperature: float):
    db_temperature = models.DBTemperature(
        city_id=city_id,
        temperature=temperature,
    )
    db.add(db_temperature)
    db.commit()
    db.refresh(db_temperature)
    return db_temperature

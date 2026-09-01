from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models, schemas


def create_city(
    db: Session,
    city: schemas.CityCreate,
) -> models.City:
    db_city = models.City(
        name=city.name,
        additional_info=city.additional_info,
    )

    db.add(db_city)
    db.commit()
    db.refresh(db_city)

    return db_city


def get_cities(db: Session) -> list[models.City]:
    statement = select(models.City)

    return db.scalars(statement).all()


def get_city(
    db: Session,
    city_id: int,
) -> models.City | None:
    return db.get(models.City, city_id)


def get_city_by_name(
    db: Session,
    name: str,
) -> models.City | None:
    statement = select(models.City).where(
        models.City.name == name
    )

    return db.scalar(statement)


def update_city(
    db: Session,
    city: models.City,
    city_data: schemas.CityUpdate,
) -> models.City:
    city.name = city_data.name
    city.additional_info = city_data.additional_info

    db.commit()
    db.refresh(city)

    return city


def delete_city(
    db: Session,
    city: models.City,
) -> None:
    db.delete(city)
    db.commit()


def get_temperatures(
    db: Session,
    city_id: int | None = None,
) -> list[models.Temperature]:
    statement = select(models.Temperature)

    if city_id is not None:
        statement = statement.where(
            models.Temperature.city_id == city_id
        )

    statement = statement.order_by(
        models.Temperature.date_time.desc()
    )

    return db.scalars(statement).all()

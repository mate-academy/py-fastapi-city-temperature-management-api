from sqlalchemy.orm import Session

from app import models, schemas


def get_city(
    db: Session,
    city_id: int,
) -> models.City | None:
    return (
        db.query(models.City)
        .filter(models.City.id == city_id)
        .first()
    )


def get_city_by_name(
    db: Session,
    name: str,
) -> models.City | None:
    return (
        db.query(models.City)
        .filter(models.City.name == name)
        .first()
    )


def get_cities(
    db: Session,
    skip: int = 0,
    limit: int = 100,
) -> list[models.City]:
    return (
        db.query(models.City)
        .offset(skip)
        .limit(limit)
        .all()
    )


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


def update_city(
    db: Session,
    db_city: models.City,
    city: schemas.CityUpdate,
) -> models.City:
    update_data = city.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(db_city, field, value)

    db.commit()
    db.refresh(db_city)

    return db_city


def delete_city(
    db: Session,
    db_city: models.City,
) -> None:
    db.delete(db_city)
    db.commit()


def create_temperature(
    db: Session,
    temperature: schemas.TemperatureCreate,
) -> models.Temperature:
    db_temperature = models.Temperature(
        city_id=temperature.city_id,
        date_time=temperature.date_time,
        temperature=temperature.temperature,
    )

    db.add(db_temperature)
    db.commit()
    db.refresh(db_temperature)

    return db_temperature


def get_temperatures(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    city_id: int | None = None,
) -> list[models.Temperature]:
    query = db.query(models.Temperature)

    if city_id is not None:
        query = query.filter(
            models.Temperature.city_id == city_id
        )

    return (
        query
        .order_by(models.Temperature.date_time.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

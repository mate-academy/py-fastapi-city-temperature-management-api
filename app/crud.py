from app import models, schemas
from sqlalchemy.orm import Session
from sqlalchemy import select


def create_city(
    db: Session,
    city: schemas.CityCreate
) -> models.City:
    db_city = models.City(**city.model_dump())
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def get_city(db: Session, city_id: int) -> models.City | None:
    city = db.get(models.City, city_id)
    return city


def get_cities(
    db: Session,
    skip: int = 0,
    limit: int = 100
) -> list[models.City]:
    stmt = select(models.City).offset(skip).limit(limit).order_by(models.City.id)
    result = db.scalars(stmt)
    cities = result.all()
    return cities


def update_city(
    db: Session,
    city_id: int,
    city: schemas.CityUpdate
) -> models.City | None:
    db_city = db.get(models.City, city_id)
    if db_city is None:
        return None
    db_city.name = city.name
    db_city.additional_info = city.additional_info
    db.commit()
    db.refresh(db_city)
    return db_city


def delete_city(
    db: Session,
    city_id: int
) -> bool:
    db_city = db.get(models.City, city_id)
    if db_city is None:
        return False
    db.delete(db_city)
    db.commit()
    return True


def get_temperatures(
    db: Session,
    city_id: int | None = None
) -> list[models.Temperature]:
    stmt = select(models.Temperature)

    if city_id is not None:
        stmt = stmt.where(models.Temperature.city_id == city_id)

    stmt = stmt.order_by(
        models.Temperature.date_time.desc(),
        models.Temperature.id.desc()
    )

    result = db.scalars(stmt)
    return list(result.all())

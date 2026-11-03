from sqlalchemy import select
from sqlalchemy.orm import Session

from app.cities import models, schemas


def get_cities(
        db: Session,
        skip: int = 0,
        limit: int = 100
) -> list[models.City]:
    return list(db.scalars(select(models.City).offset(skip).limit(limit)))


def get_city(db: Session, city_id: int) -> models.City | None:
    return db.get(models.City, city_id)


def get_city_by_name(db: Session, name: str) -> models.City | None:
    return db.scalar(select(models.City).where(models.City.name == name))


def create_city(db: Session, data: schemas.CityCreate) -> models.City:
    city = models.City(**data.model_dump())
    db.add(city)
    db.commit()
    db.refresh(city)
    return city


def update_city(
        db: Session,
        city: models.City,
        data: schemas.CityUpdate
) -> models.City:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(city, field, value)
    db.commit()
    db.refresh(city)
    return city


def delete_city(db: Session, city: models.City) -> None:
    db.delete(city)
    db.commit()

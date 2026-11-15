from sqlalchemy.orm import Session

from app.cities import models, schemas


def get_cities(db: Session) -> list[models.DBCity]:
    return db.query(models.DBCity).all()


def get_city(db: Session, city_id: int) -> models.DBCity | None:
    return (
        db.query(models.DBCity)
        .filter(models.DBCity.id == city_id)
        .first()
    )


def get_city_by_name(db: Session, name: str) -> models.DBCity | None:
    return (
        db.query(models.DBCity)
        .filter(models.DBCity.name == name)
        .first()
    )


def create_city(db: Session, city: schemas.CityCreate) -> models.DBCity:
    db_city = models.DBCity(**city.model_dump())
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def update_city(
        db: Session,
        db_city: models.DBCity,
        city: schemas.CityCreate
) -> models.DBCity:
    for field, value in city.model_dump().items():
        setattr(db_city, field, value)
    db.commit()
    db.refresh(db_city)
    return db_city


def delete_city(db: Session, db_city: models.DBCity) -> None:
    db.delete(db_city)
    db.commit()

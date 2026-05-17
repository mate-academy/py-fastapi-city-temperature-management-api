from sqlalchemy.orm import Session

from city import models, schemas


def create_city(db: Session, city: schemas.CityCreate) -> models.City:
    db_city = models.City(**city.model_dump())
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def get_cities(db: Session) -> list[models.City]:
    return db.query(models.City).order_by(models.City.id).all()


def get_city(db: Session, city_id: int) -> models.City | None:
    return db.query(models.City).filter(models.City.id == city_id).first()


def update_city(
    db: Session,
    db_city: models.City,
    city_update: schemas.CityUpdate,
) -> models.City:
    update_data = city_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_city, field, value)

    db.commit()
    db.refresh(db_city)
    return db_city


def delete_city(db: Session, db_city: models.City) -> None:
    db.delete(db_city)
    db.commit()

from sqlalchemy.orm import Session

from . import models, schemas


def get_all_cities(db: Session):
    return (db
            .query(models.DBCity)
            .all()
            )


def get_city_by_name(db: Session, name: str):
    return (db
            .query(models.DBCity)
            .filter(models.DBCity.name == name)
            .first()
            )


def get_city_by_id(db: Session, city_id: int):
    return (db
            .query(models.DBCity)
            .filter(models.DBCity.id == city_id)
            .first()
            )


def create_city(db: Session, city: schemas.CityCreate):
    db_city = models.DBCity.model_dump(city)
    db.add(db_city)
    db.commit()
    db.refresh(db_city)

    return db_city


def delete_city(db: Session, city_id: int):
    (db
     .query(models.DBCity)
     .filter(models.DBCity.id == city_id)
     .delete()
     )
    db.commit()

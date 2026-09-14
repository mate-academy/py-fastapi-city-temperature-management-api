from sqlalchemy.orm import Session

from City import models, schemas


def get_all_city(db: Session):
    return db.query(models.DBCity).all()


def get_city_by_id(db: Session, city_id: int):
    return db.query(models.DBCity).filter(models.DBCity.id == city_id).first()


def get_city_by_name(db: Session, name: str):
    return db.query(models.DBCity).filter(models.DBCity.name == name).first()


def create_city(db: Session, city: schemas.CityCreate):
    db_city_create = models.DBCity(
        name=city.name,
        additional_info=city.additional_info,
    )
    db.add(db_city_create)
    db.commit()
    db.refresh(db_city_create)

    return db_city_create


def update_city(
        db: Session,
        city: schemas.CityUpdate,
        db_city,
):
    if city.name is not None:
        db_city.name = city.name

    if city.additional_info is not None:
        db_city.additional_info = city.additional_info

    db.commit()
    db.refresh(db_city)
    return db_city


def delete_city(db: Session, db_city: models.DBCity):
    db.delete(db_city)
    db.commit()
    return db_city

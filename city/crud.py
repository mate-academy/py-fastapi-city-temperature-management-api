from sqlalchemy.orm import Session

from city import schemas, models


def create_city(db: Session, city: schemas.CityCreate):
    db_city = models.DBCity(
        name=city.name,
        additional_info=city.additional_info,
    )
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def get_all_cities(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.DBCity).offset(skip).limit(limit).all()


def get_city(db: Session, city_id: int):
    return db.query(models.DBCity).filter(
        models.DBCity.id == city_id
    ).first()


def update_city(db: Session, city_id: int, city: schemas.CityCreate):
    db_city = db.query(models.DBCity).filter(
        models.DBCity.id == city_id
    ).first()
    if db_city is None:
        return None
    db_city.name = city.name
    db_city.additional_info = city.additional_info
    db.commit()
    db.refresh(db_city)
    return db_city


def delete_city(db: Session, city_id: int):
    db_city = db.query(models.DBCity).filter(
        models.DBCity.id == city_id
    ).first()
    if db_city is None:
        return None
    db.delete(db_city)
    db.commit()
    return db_city

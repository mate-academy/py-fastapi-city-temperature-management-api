from sqlalchemy.orm import Session
from app import models, schemas


def create_city(db: Session, city: schemas.CityCreate):
    db_city = models.City(**city.model_dump())
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def get_cities(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.City).offset(skip).limit(limit).all()


def get_city(db: Session, city_id: int):
    return db.query(models.City).filter(models.City.id == city_id).first()


def update_city(db: Session, city_id: int, city_update: schemas.CityUpdate):
    db_city = get_city(db, city_id)
    if not db_city:
        return None
    for key, value in city_update.model_dump(exclude_unset=True).items():
        setattr(db_city, key, value)
    db.commit()
    db.refresh(db_city)
    return db_city


def delete_city(db: Session, city_id: int):
    db_city = get_city(db, city_id)
    if not db_city:
        return None
    db.delete(db_city)
    db.commit()
    return db_city


def create_temperature(
        db: Session,
        city_id: int,
        temp_value: float,
        date_time
):
    db_temp = models.Temperature(
        city_id=city_id,
        temperature=temp_value,
        date_time=date_time
    )
    db.add(db_temp)
    db.commit()
    db.refresh(db_temp)
    return db_temp


def get_temperatures(db: Session, city_id: int | None = None):
    query = db.query(models.Temperature)
    if city_id is not None:
        query = query.filter(models.Temperature.city_id == city_id)
    return query.all()

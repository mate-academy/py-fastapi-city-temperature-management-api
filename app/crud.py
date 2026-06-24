from sqlalchemy.orm import Session

from app import models, schemas


def get_city(db: Session, city_id: int) -> models.City | None:
    return db.query(models.City).filter(models.City.id == city_id).first()


def get_city_by_name(db: Session, name: str) -> models.City | None:
    return db.query(models.City).filter(models.City.name == name).first()


def get_cities(db: Session, skip: int = 0, limit: int = 100) -> list[models.City]:
    return db.query(models.City).offset(skip).limit(limit).all()


def create_city(db: Session, city: schemas.CityCreate) -> models.City:
    db_city = models.City(name=city.name, additional_info=city.additional_info)
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def update_city(db: Session, city_id: int, city_update: schemas.CityUpdate) -> models.City | None:
    db_city = get_city(db, city_id)
    if not db_city:
        return None
    update_data = city_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_city, field, value)
    db.commit()
    db.refresh(db_city)
    return db_city


def delete_city(db: Session, city_id: int) -> bool:
    db_city = get_city(db, city_id)
    if not db_city:
        return False
    db.delete(db_city)
    db.commit()
    return True

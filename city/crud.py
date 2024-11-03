from sqlalchemy.orm import Session

from city import models, schemas


def create_city(db: Session, city: schemas.CityCreateUpdate) -> models.City:
    db_city = models.City(**city.model_dump())
    db.add(db_city)
    db.commit()
    db.refresh(db_city)

    return db_city


def get_city(db: Session, city_id: int) -> models.City:
    return db.query(models.City).filter(models.City.id == city_id).first()


def get_city_list(
    db: Session, skip: int = 0, limit: int = 10
) -> list[models.City]:
    return db.query(models.City).offset(skip).limit(limit).all()


def get_all_cities(db: Session) -> list[models.City]:
    return db.query(models.City).all()


def update_city(
    db: Session, city_id: int, city: schemas.CityCreateUpdate
) -> models.City:
    db_city = db.query(models.City).filter(models.City.id == city_id).first()

    if db_city:
        for key, value in city.model_dump().items():
            setattr(db_city, key, value)
        db.commit()
        db.refresh(db_city)

    return db_city


def delete_city(db: Session, city_id: int) -> bool:
    db_city = db.query(models.City).filter(models.City.id == city_id).first()

    if db_city:
        db.delete(db_city)
        db.commit()
        return True

    return False

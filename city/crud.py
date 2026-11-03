from sqlalchemy.orm.session import Session

from city import models
from city import schemas


def get_all_cites(db: Session):
    return db.query(models.City).all()


def get_city_by_name(db: Session, name: str):
    return db.query(models.City).filter(models.City.name == name).first()


def create_city(db: Session, city: schemas.CityCreate):
    db_city = models.City(
        name=city.name,
        additional_info=city.additional_info,
    )
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def delete_city(db: Session, city_id: int):
    db_city = db.get(models.City, city_id)

    if not db_city:
        return False

    db.delete(db_city)
    db.commit()

    return True
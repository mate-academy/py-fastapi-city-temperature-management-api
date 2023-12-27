from sqlalchemy.orm import Session
import models, schemas


def create_city(db: Session, city: schemas.CityCreate):
    db_city = models.City(
        name=city.name,
        description=city.description,
    )
    db.add(db_city)
    db.commit()
    db.refresh(db_city)

    return db_city


def get_all_city(db: Session):
    return db.query(models.City).all()


def delete_city(db: Session, city_id: int):
    db_city = db.query(models.City).filter(models.City.id == city_id).first()
    db.delete(db_city)
    db.commit()
    get_all_city(db)

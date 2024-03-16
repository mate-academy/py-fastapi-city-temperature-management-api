from sqlalchemy.orm import Session

from city import models, schemas


def create_city(db: Session, city: schemas.CityCreate):
    db_city = models.City(name=city.name, additional_info=city.additional_info)
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def get_all_cities(db: Session):
    return db.query(models.City).all()


def get_city_by_name(db: Session, city_name: str):
    return db.query(models.City).filter(models.City.name == city_name).first()


def get_city_by_id(db: Session, city_id: int):
    return (
        db.query(models.City).filter(
            models.City.id == city_id
        ).first()
    )


def delete_city_by_id(db: Session, city_id: int):
    db.query(models.City).filter(models.City.id == city_id).delete()
    db.commit()
    return {"message": "City deleted successfully!"}


def update_city_by_id(db: Session, city: schemas.CityCreate, city_id: int):
    db.query(models.City).filter(models.City.id == city_id).update(
        {"name": city.name, "additional_info": city.additional_info}
    )
    db.commit()
    return {"message": "City updated successfully!"}

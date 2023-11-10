from fastapi import HTTPException
from sqlalchemy.orm import Session

from city import schemas, models


def get_all_cities(db: Session):
    return db.query(models.City).all()


def get_city_by_id(db: Session, city_id: int):
    return db.query(models.City).filter(models.City.id == city_id).first()


def get_city_by_name(db: Session, city_name: str):
    return (
        db.query(models.City)
        .filter(models.City.name == city_name)
        .first()
    )


def create_city(db: Session, city: schemas.CityBase):
    db_city = models.City(
        name=city.name,
        additional_info=city.additional_info
    )

    db.add(db_city)
    db.commit()
    db.refresh(db_city)

    return db_city


def update_city(db: Session, city_id: int, city: schemas.CityBase):
    db_city = db.query(models.City).filter(models.City.id == city_id).first()

    if db_city:
        for key, value in city.model_dump().items():
            setattr(db_city, key, value)

        db.commit()
        db.refresh(db_city)

        return db_city


def delete_city(db: Session, city_id: int):
    db_city = db.query(models.City).filter(models.City.id == city_id).first()

    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")

    db.delete(db_city)
    db.commit()

    return {"msg": "City deleted successfully"}

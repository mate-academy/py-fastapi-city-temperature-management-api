from fastapi import Depends
from sqlalchemy.orm import Session

import dependencies
from city.models import CityModel
from city.schemas import CitySchema


def create_city(
    city: CitySchema,
    db: Session = Depends(dependencies.get_db),
):
    db_city = CityModel(
        name=city.name,
        additional_info=city.additional_info,
    )
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def get_all_cities(db: Session):
    return db.query(CityModel).all()


def get_city_by_id(city_id: int, db: Session = Depends(dependencies.get_db)):
    return db.query(CityModel).filter(CityModel.id == city_id).first()


def update_city_by_id(db: Session, city_id: int, city: CitySchema):
    db_city = get_city_by_id(city_id=city_id, db=db)

    for attr, value in city.model_dump().items():
        setattr(db_city, attr, value)

    db.commit()
    return "City has been updated"


def delete_city_by_id(city_id: int, db: Session = Depends(dependencies.get_db)):
    db_city = get_city_by_id(city_id=city_id, db=db)
    db.delete(db_city)
    db.commit()
    return "City has been deleted"

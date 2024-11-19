from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.city import City
from app.schemas.city import CityCreate, CityUpdate


def create_city(db: Session, city: CityCreate):
    db_city = City(name=city.name, additional_info=city.additional_info)
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def get_cities(db: Session):
    return db.query(City).all()


def get_city_by_id_or_404(db: Session, city_id: int):
    db_city = db.query(City).filter(City.id == city_id).first()

    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return db_city


def get_city_by_id(db: Session, city_id: int):
    return get_city_by_id_or_404(db, city_id)


def update_city(db: Session, city_id: int, city: CityUpdate):
    db_city = get_city_by_id_or_404(db, city_id)
    db_city.name = city.name
    db_city.additional_info = city.additional_info
    db.commit()
    db.refresh(db_city)
    return db_city


def delete_city(db: Session, city_id: int):
    db_city = get_city_by_id_or_404(db, city_id)
    db.delete(db_city)
    db.commit()
    return {"message": f"City with id {city_id} was successfully deleted"}

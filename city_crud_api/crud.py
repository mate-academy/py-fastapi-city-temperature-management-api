from fastapi import HTTPException
from sqlalchemy.orm import Session

from city_crud_api.models import DBCity
from city_crud_api.schemas import CityCreate, CityUpdate


def get_city_db_by_id(db: Session, city_id: int):
    city_db = db.get(DBCity, city_id)
    if city_db is None:
        raise HTTPException(status_code=404, detail="No city with this id")
    return city_db


def get_cities(db: Session):
    return db.query(DBCity).all()


def get_city(city_id: int, db: Session):
    return get_city_db_by_id(city_id=city_id, db=db)


def create_cities(db: Session, city_schema: CityCreate):
    city_db = DBCity(
        name=city_schema.name,
        additional_info=city_schema.additional_info
    )
    db.add(city_db)
    db.commit()
    db.refresh(city_db)
    return city_db


def update_cities(city_id: int, db: Session, city_schema: CityUpdate):
    city_db = get_city_db_by_id(city_id=city_id, db=db)
    city_db.name = city_schema.name
    city_db.additional_info = city_schema.additional_info
    db.commit()
    db.refresh(city_db)
    return city_db


def delete_cities(city_id: int, db: Session):
    city_db = get_city_db_by_id(city_id=city_id, db=db)
    db.delete(city_db)
    db.commit()
    return {"ok": True}
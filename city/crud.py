from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from city import schemas
from models.city import DBCity

#----------------city--------------
def get_all_cities(db: Session):
    return db.scalars(select(DBCity)).all()


def get_city(db: Session, city_id: int):
    db_city = db.get(DBCity, city_id)
    return db_city


def create_city(db: Session, city: schemas.CityCreate):
    db_city = DBCity(
        name=city.name,
        additional_info=city.additional_info,
    )
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def delete_city(db: Session, city_id: int):
    db_city = db.get(DBCity, city_id)

    if db_city is None:
        raise HTTPException(status_code=404, detail="No such city!")
    else:
        db.delete(db_city)
        db.commit()
        return {"message": "Item deleted successfully"}

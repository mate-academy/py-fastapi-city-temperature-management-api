from fastapi import HTTPException
from sqlalchemy.orm import Session

from City import schemas
from City.models import DBCity


def create_new_city(db: Session, data_of_create: schemas.CityCreate):
    new_obj = DBCity(
        name=data_of_create.name,
        additional_info=data_of_create.additional_info,
    )

    db.add(new_obj)
    db.commit()
    db.refresh(new_obj)
    return new_obj


def city_list(db: Session):
    return db.query(DBCity).all()


def city_retrieve(db: Session, city_id: int):
    queryset = db.query(DBCity).filter(DBCity.id == city_id)
    return queryset.first()


def city_update(db: Session, city_id: int, update_city: schemas.CityUpdate):
    queryset = db.query(DBCity).filter(DBCity.id == city_id)
    update = update_city.model_dump(exclude_unset=True)
    if update:
        queryset.update(update)
    db.commit()
    return queryset.first()


def city_delete(db: Session, city_id: int):
    city = db.get(DBCity, city_id)
    if city is None:
        raise HTTPException(status_code=404, detail="Unknown city")
    db.delete(city)
    db.commit()
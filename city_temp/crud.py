from datetime import datetime
from typing import Sequence

from fastapi import HTTPException

from city_temp.models import (
    DBCity,
    DBTemperature
)
from city_temp.schemas import (
    CityCreate,
    CityUpdate,
)

from sqlalchemy import select
from sqlalchemy.orm import Session


def list_cities(db: Session) -> Sequence[DBCity]:
    return db.scalars(select(DBCity)).all()


def get_city(
        db: Session,
        city_id: int
) -> DBCity:
    city = db.scalar(
        select(DBCity).where(DBCity.id == city_id)
    )

    if city is None:
        raise HTTPException(
            status_code=404,
            detail=f"No city (id: {city_id}) found"
        )

    return city


def create_city(
        db: Session,
        new_city: CityCreate
) -> DBCity:
    db_city = DBCity(
        name=new_city.name,
        additional_info=new_city.additional_info,
    )

    db.add(db_city)
    db.commit()
    db.refresh(db_city)

    return db_city


def update_city(
        db: Session,
        city_id: int,
        updated_city: CityUpdate
) -> DBCity:
    city = get_city(
        db=db,
        city_id=city_id
    )

    city.name = updated_city.name
    city.additional_info = updated_city.additional_info

    db.commit()
    db.refresh(city)

    return city


def delete_city(
        db: Session,
        city_id: int,
) -> None:
    city = get_city(
        db=db,
        city_id=city_id
    )

    db.delete(city)
    db.commit()


def add_temperature(
        db: Session,
        city_id: int,
        date_time: datetime,
        temperature: float
) -> DBTemperature:
    obj = DBTemperature(
        city_id=city_id,
        date_time=date_time,
        temperature=temperature
    )
    db.add(obj)
    return obj


def list_temperatures(db: Session) -> Sequence[DBTemperature]:
    return db.scalars(select(DBTemperature)).all()


def list_city_temperatures(
        db: Session,
        city_id: int
) -> Sequence[DBTemperature]:
    return db.scalars(
        select(DBTemperature)
        .where(DBTemperature.city_id == city_id)
    ).all()

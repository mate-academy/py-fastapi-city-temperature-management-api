from typing import List

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette import status

import city
from city.models import CityModel
from city.schemas import CityCreateSchema, CitySchema, CityUpdateSchema, CityListSchema


def create_city(data: CityCreateSchema, db: Session) -> CitySchema:
    stmt = select(CityModel).where(CityModel.name == data.name)
    result = db.execute(stmt)
    existing_city = result.scalar_one_or_none()

    if existing_city:
        raise HTTPException(status_code=400, detail="City already exists")

    city = CityModel(
        name=data.name,
        additional_info=data.additional_info,
    )

    db.add(city)
    db.commit()
    db.refresh(city)

    return CitySchema.model_validate(city)


def get_cities(db: Session) -> List[CityListSchema]:
    stmt = select(CityModel)
    result = db.execute(stmt)
    cities = result.scalars().all()
    return [
        CityListSchema.model_validate(city)
        for city in cities
    ]


def get_city_by_id(city_id: int, db: Session) -> CitySchema:
    stmt = select(CityModel).where(CityModel.id == city_id)
    result = db.execute(stmt)
    city = result.scalar_one_or_none()

    if city is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City not found.")

    return CitySchema.model_validate(city)


def update_city(data: CityUpdateSchema, db: Session) -> CitySchema:
    stmt = select(CityModel).where(CityModel.id == data.id)
    result = db.execute(stmt)
    city = result.scalar_one_or_none()

    if city is None:
        raise HTTPException(status_code=404, detail="City not found.")

    city.name = data.name
    city.additional_info = data.additional_info

    db.add(city)
    db.commit()
    db.refresh(city)

    return CitySchema.model_validate(city)


def delete_city_from_db(city_id: int, db: Session) -> CitySchema:
    stmt = select(CityModel).where(CityModel.id == city_id)
    result = db.execute(stmt)
    city = result.scalar_one_or_none()

    if city is None:
        raise HTTPException(status_code=404, detail="City not found.")

    db.delete(city)
    db.commit()

    return CitySchema.model_validate(city)

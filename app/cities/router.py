from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.cities.models import City
from app.cities.schemas import CityRead, CityCreate
from app.db.database import get_db


router = APIRouter()

@router.get("", response_model=list[CityRead])
def get_cities(db: Session = Depends(get_db)):
    return db.query(City).all()

@router.get("/{city_id}", response_model=CityRead)
def get_city(city_id: int, db: Session = Depends(get_db)):
    city = db.query(City).filter(City.id == city_id).first()

    if city is None:
        raise HTTPException(
            status_code=404,
            detail="City not found"
        )

    return city

@router.post(
    "",
    response_model=CityRead,
    status_code=201
)
def post_city(
        new_city: CityCreate,
        db: Session = Depends(get_db)
):
    try:
        city = City(**new_city.model_dump())
        db.add(city)
        db.commit()
        db.refresh(city)

        return city

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Database operation failed"
        )

@router.put("/{city_id}", response_model=CityRead)
def update_city(
    city_id: int,
    fields_to_update: CityCreate,
    db: Session = Depends(get_db)
):
    try:
        city_to_update = db.query(City).filter(City.id == city_id).first()

        if city_to_update is None:
            raise HTTPException(
                status_code=404,
                detail="City not found"
            )

        for field, value in fields_to_update.model_dump().items():
            setattr(city_to_update, field, value)
        db.commit()
        db.refresh(city_to_update)

        return city_to_update

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Database operation failed"
        )

@router.delete("/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_city(city_id: int, db: Session = Depends(get_db)):
    try:
        city_to_delete = db.query(City).filter(City.id == city_id).first()
        if city_to_delete is None:
            raise HTTPException(
                status_code=404,
                detail="City not found"
            )
        db.delete(city_to_delete)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Database operation failed"
        )

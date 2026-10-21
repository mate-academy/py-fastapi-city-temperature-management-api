from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db


router = APIRouter(prefix="/cities", tags=["Cities"])


@router.post("", response_model=schemas.City, status_code=status.HTTP_201_CREATED)
def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)):
    new_city = models.City(**city.model_dump())

    db.add(new_city)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="City with this name already exists",
        )

    db.refresh(new_city)
    return new_city


@router.get("", response_model=list[schemas.City])
def get_cities(db: Session = Depends(get_db)):
    return db.scalars(select(models.City)).all()


@router.get("/{city_id}", response_model=schemas.City)
def get_city(city_id: int, db: Session = Depends(get_db)):
    city = db.get(models.City, city_id)

    if city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return city


@router.put("/{city_id}", response_model=schemas.City)
def update_city(
    city_id: int,
    city_data: schemas.CityUpdate,
    db: Session = Depends(get_db),
):
    city = db.get(models.City, city_id)

    if city is None:
        raise HTTPException(status_code=404, detail="City not found")

    for field, value in city_data.model_dump().items():
        setattr(city, field, value)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="City with this name already exists",
        )

    db.refresh(city)
    return city


@router.delete("/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_city(city_id: int, db: Session = Depends(get_db)):
    city = db.get(models.City, city_id)

    if city is None:
        raise HTTPException(status_code=404, detail="City not found")

    db.delete(city)
    db.commit()

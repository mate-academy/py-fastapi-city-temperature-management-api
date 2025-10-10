from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas
from ..deps import get_db
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix="/cities", tags=["cities"])


@router.post(
    "",
    response_model=schemas.CityOut,
    status_code=status.HTTP_201_CREATED
)
def create_city(payload: schemas.CityCreate, db: Session = Depends(get_db)):
    city = models.City(
        name=payload.name.strip(),
        additional_info=payload.additional_info
    )
    db.add(city)
    try:
        db.commit()
        db.refresh(city)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="City with this name already exists."
        )
    return city


@router.get("", response_model=List[schemas.CityOut])
def list_cities(db: Session = Depends(get_db)):
    return db.query(models.City).order_by(models.City.name.asc()).all()


@router.get("/{city_id}", response_model=schemas.CityOut)
def get_city(city_id: int, db: Session = Depends(get_db)):
    city = db.get(models.City, city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@router.put("/{city_id}", response_model=schemas.CityOut)
def update_city(
        city_id: int,
        payload: schemas.CityUpdate,
        db: Session = Depends(get_db)
):
    city = db.get(models.City, city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    if payload.name is not None:
        city.name = payload.name.strip()
    if payload.additional_info is not None:
        city.additional_info = payload.additional_info
    try:
        db.commit()
        db.refresh(city)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="City with this name already exists."
        )
    return city


@router.delete(
    "/{city_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_city(city_id: int, db: Session = Depends(get_db)):
    city = db.get(models.City, city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    db.delete(city)
    db.commit()
    return None

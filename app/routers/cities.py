from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app import schemas
from app.database import get_db
from app.models import City

router = APIRouter(prefix="/cities", tags=["cities"])


@router.post("/", response_model=schemas.CityOut, status_code=status.HTTP_201_CREATED)
def create_city(payload: schemas.CityCreate, db: Session = Depends(get_db)):
    existing = db.query(City).filter(City.name == payload.name).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="City with this name already exists.")

    city = City(name=payload.name, additional_info=payload.additional_info)
    db.add(city)
    db.commit()
    db.refresh(city)
    return city


@router.get("/", response_model=List[schemas.CityOut])
def list_cities(db: Session = Depends(get_db)):
    return db.query(City).order_by(City.id.asc()).all()


@router.get("/{city_id}", response_model=schemas.CityOut)
def get_city(city_id: int, db: Session = Depends(get_db)):
    city = db.get(City, city_id)
    if not city:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City not found.")
    return city


@router.put("/{city_id}", response_model=schemas.CityOut)
def update_city(city_id: int, payload: schemas.CityUpdate, db: Session = Depends(get_db)):
    city = db.get(City, city_id)
    if not city:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City not found.")

    if payload.name and payload.name != city.name:
        duplicate = db.query(City).filter(City.name == payload.name).first()
        if duplicate:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Another city with this name exists.")
        city.name = payload.name

    if payload.additional_info is not None:
        city.additional_info = payload.additional_info

    db.add(city)
    db.commit()
    db.refresh(city)
    return city


@router.delete("/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_city(city_id: int, db: Session = Depends(get_db)):
    city = db.get(City, city_id)
    if not city:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City not found.")

    db.delete(city)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


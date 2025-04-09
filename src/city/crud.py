from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from src.city.models import CityModel
from src.city.schemas import CityCreateSchema
from src.database import get_db


def create_city(city: CityCreateSchema, db: Session = Depends(get_db)):
    db_city = db.query(CityModel).filter(CityModel.name == city.name).first()
    if db_city:
        raise HTTPException(
            status_code=400,
            detail=f"City with name '{city.name}' already exists"
        )
    db_city = CityModel(**city.model_dump())
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def get_cities(db: Session = Depends(get_db)):
    return db.query(CityModel).all()


def get_city(city_id: int, db: Session = Depends(get_db)):
    city = db.query(CityModel).filter(CityModel.id == city_id).first()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city


def put_city(
        city_id: int,
        city_data: CityCreateSchema,
        db: Session = Depends(get_db)
):
    city = db.query(CityModel).filter(CityModel.id == city_id).first()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    for key, value in city_data.model_dump().items():
        setattr(city, key, value)

    db.commit()
    db.refresh(city)
    return city


def delete_city(city_id: int, db: Session = Depends(get_db)):
    city = db.query(CityModel).filter(CityModel.id == city_id).first()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    db.delete(city)
    db.commit()

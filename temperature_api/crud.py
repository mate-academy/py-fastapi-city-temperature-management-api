from fastapi import Depends
from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.future import engine
from sqlalchemy.orm import sessionmaker, Session
from typing import List


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/cities/", response_model=City)
def create_city(city: CityCreate, db: Session = Depends(get_db)):
    db_city = City(**city.model_dump())
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


@app.get("/cities/{city_id}", response_model=City)
def read_city(city_id: int, db: Session = Depends(get_db)):
    city = db.query(City).filter(City.id == city_id).first()
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@app.put("/cities/{city_id}", response_model=City)
def update_city(city_id: int, city: CityCreate, db: Session = Depends(get_db)):
    db_city = db.query(City).filter(City.id == city_id).first()
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    for key, value in city.dict().items():
        setattr(db_city, key, value)
    db.commit()
    db.refresh(db_city)
    return db_city


@app.delete("/cities/{city_id}", response_model=City)
def delete_city(city_id: int, db: Session = Depends(get_db)):
    db_city = db.query(City).filter(City.id == city_id).first()
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    db.delete(db_city)
    db.commit()
    return db_city


@app.get("/cities/", response_model=List[City])
def list_cities(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    cities = db.query(City).offset(skip).limit(limit).all()
    return cities

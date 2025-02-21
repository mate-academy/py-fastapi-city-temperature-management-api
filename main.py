from datetime import datetime

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql import crud

from engine import engine, SessionLocal
from database import Base

import crud
from models import City, Temperature
from schemas import CityCreate

app = FastAPI()

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

@app.post("/cities/")
def create_city(city: CityCreate, db: Session = Depends(get_db)):
    return crud.create_city(db, city)

@app.post("/temperatures/update")
async def update_temperature_for_all_cities(db: Session = Depends(get_db)):
    cities = db.query(City).all()

    for city in cities:
        temperature_data = await fetch_temperature_from_api(city.name)
        temperature = Temperature(city_id=city.id, date_time=datetime.now(), temperature=temperature_data)
        db.add(temperature)

    db.commit()
    return {"message": "Temperatures updated successfully"}
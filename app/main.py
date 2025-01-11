from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .db import SessionLocal, init_db
from .utils import fetch_temperature

app = FastAPI()

init_db()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# CRUD API для City
@app.post("/cities/", response_model=schemas.City)
def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)):
    return crud.create_city(db=db, city=city)


@app.get("/cities/", response_model=list[schemas.City])
def read_cities(db: Session = Depends(get_db)):
    return crud.get_cities(db=db)


@app.delete("/cities/{city_id}", response_model=schemas.City)
def delete_city(city_id: int, db: Session = Depends(get_db)):
    city = crud.delete_city(db=db, city_id=city_id)
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@app.post("/temperatures/update")
async def update_temperatures(db: Session = Depends(get_db)):
    cities = crud.get_cities(db)
    for city in cities:
        temperature = await fetch_temperature(city.name)
        crud.create_temperature(db, schemas.TemperatureCreate(city_id=city.id, temperature=temperature))
    return {"message": "Temperatures updated"}


@app.get("/temperatures/", response_model=list[schemas.Temperature])
def get_temperatures(city_id: int = None, db: Session = Depends(get_db)):
    return crud.get_temperatures(db=db, city_id=city_id)

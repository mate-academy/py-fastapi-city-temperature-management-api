from typing import List
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine
import asyncio

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/cities", response_model=schemas.City)
def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)):
    return crud.create_city(db, city)


@app.get("/cities", response_model=List[schemas.City])
def read_cities(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_cities(db, skip=skip, limit=limit)


@app.get("/cities/{city_id}", response_model=schemas.City)
def read_city(city_id: int, db: Session = Depends(get_db)):
    db_city = crud.get_city(db, city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city


@app.put("/cities/{city_id}", response_model=schemas.City)
def update_city(city_id: int, city: schemas.CityCreate, db: Session = Depends(get_db)):
    return crud.update_city(db, city_id, city)


@app.delete("/cities/{city_id}", response_model=schemas.City)
def delete_city(city_id: int, db: Session = Depends(get_db)):
    return crud.delete_city(db, city_id)


@app.post("/temperatures/update")
async def update_temperatures(db: Session = Depends(get_db)):
    cities = crud.get_cities(db)
    for city in cities:
        temp = await crud.fetch_temperature(city.name)
        crud.create_temperature(db, city.id, temp)
    return {"message": "Temperatures updated"}


@app.get("/temperatures", response_model=List[schemas.Temperature])
def get_temperatures(city_id: int = None, db: Session = Depends(get_db)):
    return crud.get_temperatures(db, city_id=city_id)
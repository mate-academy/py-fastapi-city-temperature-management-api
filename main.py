from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import httpx
from datetime import datetime

import crud
import models
import schemas
from database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/cities/", response_model=schemas.City)
def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)):
    return crud.create_city(db=db, city=city)

@app.get("/cities/", response_model=List[schemas.City])
def read_cities(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_cities(db, skip=skip, limit=limit)

@app.delete("/cities/{city_id}")
def delete_city(city_id: int, db: Session = Depends(get_db)):
    db_city = crud.delete_city(db, city_id=city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return {"message": "City deleted successfully"}

@app.get("/temperatures/", response_model=List[schemas.Temperature])
def read_temperatures(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_temperatures(db, skip=skip, limit=limit)

@app.put("/temperatures/update")
async def update_temperature(db: Session = Depends(get_db)):
    cities = crud.get_cities(db)

    async with httpx.AsyncClient() as client:
        for city in cities:
            temp_val = 20.0

            temp_data = schemas.TemperatureCreate(
                city_id=city.id,
                date_time=datetime.now(),
                temperature=temp_val
            )
            crud.create_temperature(db, temp_data)

    return {"message": "Temperature database updated for all cities."}

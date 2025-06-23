from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine, Base
from typing import List, Optional
import services
import asyncio

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- City Endpoints ---
@app.post("/cities/", response_model=schemas.City)
def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)):
    return crud.create_city(db, city)


@app.get("/cities/", response_model=List[schemas.City])
def list_cities(db: Session = Depends(get_db)):
    return crud.get_cities(db)


@app.get("/cities/{city_id}", response_model=schemas.City)
def get_city(city_id: int, db: Session = Depends(get_db)):
    city = crud.get_city(db, city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@app.put("/cities/{city_id}", response_model=schemas.City)
def update_city(city_id: int, city: schemas.CityCreate, db: Session = Depends(get_db)):
    updated = crud.update_city(db, city_id, city)
    if not updated:
        raise HTTPException(status_code=404, detail="City not found")
    return updated


@app.delete("/cities/{city_id}")
def delete_city(city_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_city(db, city_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="City not found")
    return {"message": "City deleted"}


# --- Temperature Endpoints ---
@app.post("/temperatures/update")
async def update_temperatures(db: Session = Depends(get_db)):
    cities = crud.get_cities(db)
    for city in cities:
        temp = await services.fetch_temperature(city.name)
        crud.create_temperature(db, city.id, temp)
    return {"status": "Temperatures updated"}


@app.get("/temperatures/", response_model=List[schemas.Temperature])
def list_temperatures(city_id: Optional[int] = None, db: Session = Depends(get_db)):
    return crud.get_temperatures(db, city_id)

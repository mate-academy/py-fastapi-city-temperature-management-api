from datetime import datetime
from typing import List, Optional

import httpx
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="City Temperature Management API")

WEATHER_API_URL = (
    "https://wttr.in/{city}?format=j1"
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- City endpoints ---

@app.post("/cities/", response_model=schemas.City, status_code=201)
def create_city(
    city: schemas.CityCreate, db: Session = Depends(get_db)
):
    return crud.create_city(db=db, city=city)


@app.get("/cities/", response_model=List[schemas.City])
def read_cities(db: Session = Depends(get_db)):
    return crud.get_cities(db=db)


@app.get("/cities/{city_id}", response_model=schemas.City)
def read_city(city_id: int, db: Session = Depends(get_db)):
    db_city = crud.get_city(db=db, city_id=city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city


@app.put("/cities/{city_id}", response_model=schemas.City)
def update_city(
    city_id: int,
    city: schemas.CityUpdate,
    db: Session = Depends(get_db),
):
    db_city = crud.update_city(db=db, city_id=city_id, city=city)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city


@app.delete("/cities/{city_id}", response_model=schemas.City)
def delete_city(city_id: int, db: Session = Depends(get_db)):
    db_city = crud.delete_city(db=db, city_id=city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city


# --- Temperature endpoints ---

@app.post("/temperatures/update")
async def update_temperatures(db: Session = Depends(get_db)):
    cities = crud.get_cities(db=db)
    if not cities:
        return {"message": "No cities in the database"}

    results = []
    async with httpx.AsyncClient() as client:
        for city in cities:
            try:
                response = await client.get(
                    WEATHER_API_URL.format(city=city.name),
                    timeout=10,
                )
                response.raise_for_status()
                data = response.json()
                temp_c = float(
                    data["current_condition"][0]["temp_C"]
                )
                temp_record = crud.create_temperature(
                    db=db,
                    temp=schemas.TemperatureCreate(
                        city_id=city.id,
                        date_time=datetime.now(),
                        temperature=temp_c,
                    ),
                )
                results.append(
                    {"city": city.name, "temperature": temp_c}
                )
            except Exception as e:
                results.append(
                    {"city": city.name, "error": str(e)}
                )

    return {"updated": results}


@app.get("/temperatures/", response_model=List[schemas.Temperature])
def read_temperatures(
    city_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    return crud.get_temperatures(db=db, city_id=city_id)

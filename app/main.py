from fastapi import FastAPI, Depends, HTTPException

from app.database import Base, engine
from app import models, crud, schemas, dependencies
import app.models
from sqlalchemy.orm import Session
from app.weather import update_city_temperatures


app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.post("/cities", response_model=schemas.CityResponse)
def create_city(
        city: schemas.CityCreate,
        db: Session = Depends(dependencies.get_db)
) -> models.City:
    return crud.create_city(db=db, city=city)

@app.get("/cities", response_model=list[schemas.CityResponse])
def read_cities(
        db: Session = Depends(dependencies.get_db),
) -> list[schemas.CityResponse]:
    return crud.get_cities(db=db)

@app.get("/cities/{city_id}", response_model=schemas.CityResponse)
def read_city(
        city_id: int,
        db: Session = Depends(dependencies.get_db),
) -> models.City:
    db_city = crud.get_city_by_id(db=db, city_id=city_id)

    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return db_city

@app.put("/cities/{city_id}", response_model=schemas.CityResponse)
def update_city(
        city_id: int,
        city: schemas.CityCreate,
        db: Session = Depends(dependencies.get_db),
) -> models.City:
    db_city = crud.update_city(db=db, city_id=city_id, city=city)

    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return db_city

@app.delete("/cities/{city_id}", response_model=schemas.CityResponse)
def delete_city(
        city_id: int,
        db: Session = Depends(dependencies.get_db),
) -> models.City:
    db_city = crud.delete_city(db=db, city_id=city_id)

    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return db_city

@app.post("/temperatures/update", response_model=list[schemas.TemperatureResponse])
async def update_temperatures(
        db: Session = Depends(dependencies.get_db)
) -> list[models.Temperature]:
    cities = crud.get_cities(db=db)

    temperature_records = await update_city_temperatures(db=db, cities=cities)

    return temperature_records

@app.get("/temperatures", response_model=list[schemas.TemperatureResponse])
def read_temperatures(
        city_id: int | None = None,
        db: Session = Depends(dependencies.get_db)
) -> list[models.Temperature]:
    return crud.get_temperatures(db=db, city_id=city_id)
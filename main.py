from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="City Temperature API")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/cities/", response_model=schemas.City, status_code=201)
def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)):
    db_city = crud.get_city_by_name(db, city_name=city.name)
    if db_city:
        raise HTTPException(status_code=400, detail="City already exists")
    return crud.create_city(db=db, city=city)


@app.get("/cities/", response_model=list[schemas.City])
def read_cities(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    cities = crud.get_cities(db, skip=skip, limit=limit)
    return cities


@app.post(
    "/temperatures/",
    response_model=schemas.Temperature,
    status_code=201,
)
def create_temperature(
    temperature: schemas.TemperatureCreate, db: Session = Depends(get_db)
):
    db_city = crud.get_city(db, city_id=temperature.city_id)
    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")
    return crud.create_temperature(db=db, temperature=temperature)


@app.get("/temperatures/", response_model=list[schemas.Temperature])
def read_temperatures(
    city_id: int | None = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    temperatures = crud.get_temperature(db, city_id=city_id, skip=skip, limit=limit)
    return temperatures


@app.post("/temperatures/update", status_code=200)
async def update_temperatures(db: Session = Depends(get_db)):
    from datetime import datetime
    from weather_service import fetch_city_temperature

    cities = crud.get_cities(db)
    updated_count = 0

    for city in cities:
        temp = await fetch_city_temperature(city.name)
        if temp is not None:
            temp_in = schemas.TemperatureCreate(
                city_id=city.id,
                date_time=datetime.utcnow(),
                temperature=temp,
            )
            crud.create_temperature(db, temperature=temp_in)
            updated_count += 1

    return {
        "message": "Temperatures updated successfully",
        "updated_cities": updated_count,
    }


@app.delete("/cities/{city_id}", status_code=204)
def delete_city(city_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_city(db=db, city_id=city_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="City not found")

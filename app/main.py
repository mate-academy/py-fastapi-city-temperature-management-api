from typing import List

from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException

from app import crud
from app import schemas
from app.db.db_creating import get_db
from app.router import router

app = FastAPI()
app.include_router(router)


@app.get("/cities/", response_model=list[schemas.City])
def get_cities(skip: int = 0,
               limit: int = 10,
               db: Session = Depends(get_db))\
        -> List[schemas.City]:
    return crud.get_all_cities(db, skip=skip, limit=limit)


@app.post("/cities/", response_model=schemas.City)
def create_city(city: schemas.CityCreate,
                db: Session = Depends(get_db))\
        -> schemas.City:
    return crud.create_city(db=db, city=city)


@app.get("/cities/{city_id}/", response_model=schemas.City)
def get_city_by_id(city_id: int, db: Session = Depends(get_db))\
        -> schemas.City:
    db_city = crud.get_city_by_id(db=db, city_id=city_id)

    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")

    return db_city


@app.put("/cities/{city_id}/", response_model=schemas.City)
def upgrade_city_by_id(city_id: int,
                       city: schemas.CityCreate,
                       db: Session = Depends(get_db)):
    db_city = crud.update_city(city_id=city_id, city=city, db=db)

    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")

    return db_city


@app.delete("/cities/{city_id}/", response_model=schemas.City)
def delete_city_by_id(city_id: int,
                      db: Session = Depends(get_db)):
    db_city = crud.delete_city(city_id=city_id, db=db)

    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")

    return db_city


@app.get("/temperatures/", response_model=list[schemas.Temperature])
def get_temperatures(skip: int = 0,
                     limit: int = 10,
                     db: Session = Depends(get_db)):
    return crud.get_all_temperature(db, skip=skip, limit=limit)


@app.get("/temperatures/?city_id={city_id}", response_model=schemas.Temperature)
def get_temperature_by_city_id(city_id: int, db: Session = Depends(get_db))\
        -> List[schemas.Temperature]:
    db_temperature = crud.get_temperatures_by_city_id(db=db, city_id=city_id)

    return db_temperature

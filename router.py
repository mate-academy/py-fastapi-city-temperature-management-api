from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import base, engine, SessionLocal
from temperature_parser import get_temperature_data

app = FastAPI()


base.metadata.create_all(bind=engine)


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/cities/", response_model=list[schemas.CityList])
def city_list(db: Session = Depends(get_db)):
    return crud.get_all_cities(db=db)


@app.post("/cities/", response_model=schemas.CityList)
def city_create(
    city: schemas.CityCreate,
    db: Session = Depends(get_db)
):
    return crud.create_city(db=db, city=city)


@app.get("/cities/{city_id}/", response_model=schemas.CityList)
def city_detail(city_id: int, db: Session = Depends(get_db)):
    city = crud.get_city(db=db, city_id=city_id)

    if not city:
        return HTTPException(status_code=404, detail="The city was not found")

    return city


@app.put("/cities/{city_id}/", response_model=schemas.CityList)
def city_update(city_id: int, city_update: schemas.CityUpdate, db: Session = Depends(get_db)):
    city = crud.update_city(db=db, city_id=city_id, city_to_update=city_update)

    if not city:
        return HTTPException(status_code=404, detail="The city was not found")

    return city


@app.delete("/cities/{city_id}/", response_model=schemas.CityList)
def city_delete(city_id: int, db: Session = Depends(get_db)):
    return crud.delete_city(db=db, city_id=city_id)


@app.get("/temperature/", response_model=list[schemas.TemperatureList])
def temperatures_list(db: Session = Depends(get_db)):
    return crud.get_all_cities(db=db)


def get_cities(db: Session = Depends(get_db)):
    return db.scalars(select(models.City)).all()


@app.post("/temperatures/update/", response_model=schemas.TemperatureList)
async def temperature_create(db: Session = Depends(get_db), cities = Depends(get_cities)):
    return await get_temperature_data(db=db, cities=cities)

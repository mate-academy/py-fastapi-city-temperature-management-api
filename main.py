import asyncio
from datetime import datetime

import httpx
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

import crud
from database import get_db, Base, engine
from models import City, Temperature
from schemas import CityCreate, CityRead, TemperatureCreate, TemperatureRead
from weather import get_current_temperature

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/cities/")
def get_cities(session: Session = Depends(get_db)):
    return crud.get_all_cities(session)


@app.post("/cities/", response_model=CityRead, status_code=201)
def create_city(city_data: CityCreate, session: Session = Depends(get_db)):
    city = crud.create_city(session, city_data)

    return city


@app.get("/cities/{city_id}/", response_model=CityRead)
def get_city_by_id(city_id: int, session: Session = Depends(get_db)):
    city = crud.get_city_by_id(session, city_id)
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return city


@app.delete("/cities/{city_id}/", status_code=204)
def delete_city(city_id: int, session: Session = Depends(get_db)):
    result = crud.delete_city(session, city_id)
    if result is False:
        raise HTTPException(status_code=404, detail="City not found")

    return


@app.put("/cities/{city_id}/", response_model=CityRead)
def update_city(city_id: int, city_data: CityCreate, session: Session = Depends(get_db)):
    city = crud.update_city(session, city_id, city_data)
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@app.post("/temperatures/update/")
async def update_temperatures(session: Session = Depends(get_db)):
    cities = crud.get_all_cities(session)

    coroutines = []
    for city in cities:
        coroutines.append(get_current_temperature(city.name))

    try:
        temperatures = await asyncio.gather(*coroutines)
    except httpx.HTTPError:
        raise HTTPException(status_code=502, detail="Bad Gateway")

    city_temperatures = zip(cities, temperatures)

    for city, temperature in city_temperatures:
        data = TemperatureCreate(city_id=city.id, temperature=temperature, date_time=datetime.now())
        result = Temperature(**data.model_dump())
        session.add(result)

    try:
        session.commit()
    except SQLAlchemyError:
        session.rollback()
        raise HTTPException(status_code=500)


    return {"updated": len(temperatures)}


@app.get("/temperatures/", response_model=list[TemperatureRead])
def get_temperatures(session: Session = Depends(get_db), city_id: int | None = None):
    return crud.get_temperatures(session=session, city_id=city_id)
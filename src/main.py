import asyncio
import datetime

from typing import Annotated

import httpx
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session


import schemas
from crud import cities, temperatures
from db import models
from db.session import get_db
from services import fetch_current_temperature

app = FastAPI()

SessionDP = Annotated[Session, Depends(get_db)]


@app.post("/temperatures/update/")
async def update_temperatures(db: SessionDP):
    db_cities = cities.get_all_cities(db)
    async with httpx.AsyncClient() as client:
        res = await asyncio.gather(
            *(
                fetch_current_temperature(city_name=city.name, client=client)
                for city in db_cities
            )
        )
    now = datetime.datetime.now(datetime.timezone.utc)
    updated, failed = 0, []
    for city, temp in zip(db_cities, res):
        if temp is None:
            failed.append(city.name)
            continue
        db.add(
            models.Temperature(
                city_id=city.id, date_time=now, temperature=temp
            )
        )
        updated += 1
    db.commit()
    return {"updated": updated, "failed": failed}


@app.post("/cities/", response_model=schemas.City, status_code=201)
def city_create(db: SessionDP, city_data: schemas.CityCreate):
    city = cities.get_city_by_name(db=db, city_name=city_data.name)
    if city:
        raise HTTPException(status_code=400, detail="City already exists")
    return cities.create_city(city_data=city_data, db=db)


@app.get("/cities/", response_model=list[schemas.City])
def get_all_cities(db: SessionDP):
    return cities.get_all_cities(db=db)


@app.get("/cities/{city_id}/", response_model=schemas.City)
def retrieve_city(db: SessionDP, city_id: int):
    city = cities.get_city_by_id(db=db, city_id=city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@app.delete("/cities/{city_id}/", status_code=204)
def delete_city(db: SessionDP, city_id: int):
    city = cities.get_city_by_id(db=db, city_id=city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    cities.delete_city(db=db, city_id=city_id)


@app.get("/temperatures/", response_model=list[schemas.Temperature])
def read_temperatures(db: SessionDP, city_id: int | None = None):
    if city_id is None:
        return temperatures.get_all_temperatures(db=db)

    if cities.get_city_by_id(db=db, city_id=city_id) is None:
        raise HTTPException(status_code=404, detail="City not found")

    return temperatures.get_temperatures_by_city_id(db=db, city_id=city_id)

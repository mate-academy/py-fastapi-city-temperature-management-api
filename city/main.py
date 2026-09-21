from datetime import datetime

import httpx

from fastapi import FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi.params import Depends
from city.database import Base, engine

import schemas
from city import models
from city.crud import is_city_in_db, create_new_city, put_city, del_city
from city.database import SessionLocal


Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.post("/cities/", response_model=schemas.City)
def create_city(city_data: schemas.CityBase, db: Session = Depends(get_db)):
    res = is_city_in_db(db=db, city_name=city_data.name)

    if res:
        raise HTTPException(
            status_code=400,
            detail="Such city is in database"
        )
    return create_new_city(db=db, city_data=city_data)


@app.get("/cities/", response_model=list[schemas.City])
def get_all_cities(db: Session = Depends(get_db)):
    return db.scalars(select(models.City)).all()


@app.get("/cities/{city_id}/", response_model=schemas.City)
def get_city(city_id: int, db: Session = Depends(get_db)):
    res = db.get(models.City, city_id)

    if not res:
        raise HTTPException(status_code=404, detail="Not found")

    return res


@app.put("/cities/{city_id}/", response_model=schemas.City)
def update_city(city_id: int, city_data: schemas.CityBase, db: Session = Depends(get_db)):
    city = put_city(db=db, city_data=city_data, city_id=city_id)

    if city is None:
        raise HTTPException(status_code=404, detail="Not Found")

    return city


@app.delete("/cities/{city_id}")
def delete_city(
    city_id: int,
    db: Session = Depends(get_db),
):
    city = del_city(db, city_id)

    if city is None:
        raise HTTPException(404, "City not found")

    return {"detail": "City deleted"}


async def get_coordinates(city_name: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={
                "name": city_name,
                "count": 1,
            },
        )

        response.raise_for_status()

        data = response.json()

        if not data.get("results"):
            return None

        city = data["results"][0]

        return city["latitude"], city["longitude"]


async def get_temperature(city_name: str):
    coordinates = await get_coordinates(city_name)

    if coordinates is None:
        return None

    latitude, longitude = coordinates

    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current": "temperature_2m",
            },
        )

        response.raise_for_status()

        data = response.json()

        return data["current"]["temperature_2m"]


@app.post("/temperatures/update/")
async def update_temperatures(db: Session = Depends(get_db)):
    cities = db.scalars(select(models.City)).all()

    for city in cities:
        temperature = await get_temperature(city.name)

        if temperature is None:
            continue

        db_temperature = models.Temperature(
            city_id=city.id,
            date_time=datetime.now(),
            temperature=temperature,
        )

        db.add(db_temperature)

    db.commit()

    return {"detail": "Temperatures updated"}


@app.get(
    "/temperatures/",
    response_model=list[schemas.Temperature],
)
def get_temperatures(
    city_id: int | None = None,
    db: Session = Depends(get_db),
):
    query = select(models.Temperature)

    if city_id is not None:
        query = query.where(
            models.Temperature.city_id == city_id
        )

    return db.scalars(query).all()

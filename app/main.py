import asyncio
from contextlib import asynccontextmanager

import httpx
from fastapi import Depends, FastAPI, HTTPException, Response
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import Base, engine, get_db
from app.weather import WeatherError, fetch_temperature, get_weather_client


@asynccontextmanager
async def lifespan(_app: FastAPI):
    Base.metadata.create_all(engine)
    yield


app = FastAPI(title="City Temperature Management API", lifespan=lifespan)


@app.post("/cities", response_model=schemas.CityRead, status_code=201)
def create_city(data: schemas.CityCreate, db: Session = Depends(get_db)) -> models.City:
    city = models.City(**data.model_dump())
    db.add(city)
    db.commit()
    db.refresh(city)
    return city


@app.get("/cities", response_model=list[schemas.CityRead])
def list_cities(db: Session = Depends(get_db)) -> list[models.City]:
    return list(db.scalars(select(models.City).order_by(models.City.id)))


@app.delete("/cities/{city_id}", status_code=204)
def delete_city(city_id: int, db: Session = Depends(get_db)) -> Response:
    city = db.get(models.City, city_id)
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    db.delete(city)
    db.commit()
    return Response(status_code=204)


@app.post("/temperatures/update", response_model=list[schemas.TemperatureRead])
async def update_temperatures(
    db: Session = Depends(get_db), weather: httpx.AsyncClient = Depends(get_weather_client)
) -> list[models.Temperature]:
    cities = list(db.scalars(select(models.City).order_by(models.City.id)))
    try:
        readings = await asyncio.gather(*(fetch_temperature(weather, city.name) for city in cities))
    except WeatherError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    records = [models.Temperature(city_id=city.id, date_time=reading[0], temperature=reading[1])
               for city, reading in zip(cities, readings)]
    db.add_all(records)
    db.commit()
    for record in records:
        db.refresh(record)
    return records


@app.get("/temperatures", response_model=list[schemas.TemperatureRead])
def list_temperatures(city_id: int | None = None, db: Session = Depends(get_db)) -> list[models.Temperature]:
    query = select(models.Temperature).order_by(models.Temperature.id)
    if city_id is not None:
        query = query.where(models.Temperature.city_id == city_id)
    return list(db.scalars(query))

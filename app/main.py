from datetime import datetime

import httpx
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import Base, engine, get_db


Base.metadata.create_all(bind=engine)

app = FastAPI(title="City Temperature Management API")


@app.post("/cities", response_model=schemas.City)
def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)):
    db_city = models.City(name=city.name, additional_info=city.additional_info)
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


@app.get("/cities", response_model=list[schemas.City])
def get_cities(db: Session = Depends(get_db)):
    return db.query(models.City).all()


@app.delete("/cities/{city_id}")
def delete_city(city_id: int, db: Session = Depends(get_db)):
    city = db.query(models.City).filter(models.City.id == city_id).first()
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")

    db.delete(city)
    db.commit()
    return {"message": "City deleted"}


async def fetch_temperature(city_name: str):
    async with httpx.AsyncClient() as client:
        try:
            geo_response = await client.get(
                "https://geocoding-api.open-meteo.com/v1/search",
                params={"name": city_name, "count": 1},
            )
            geo_response.raise_for_status()
            results = geo_response.json().get("results")
            if not results:
                return None

            latitude = results[0]["latitude"]
            longitude = results[0]["longitude"]

            weather_response = await client.get(
                "https://api.open-meteo.com/v1/forecast",
                params={
                    "latitude": latitude,
                    "longitude": longitude,
                    "current": "temperature_2m",
                },
            )
            weather_response.raise_for_status()
            current = weather_response.json()["current"]
            return {
                "temperature": current["temperature_2m"],
                "date_time": datetime.fromisoformat(current["time"]),
            }
        except (httpx.HTTPError, KeyError, ValueError):
            return None


@app.post("/temperatures/update", response_model=list[schemas.Temperature])
async def update_temperatures(db: Session = Depends(get_db)):
    cities = db.query(models.City).all()
    temperatures = []

    for city in cities:
        current_temperature = await fetch_temperature(city.name)
        if current_temperature is None:
            continue

        db_temperature = models.Temperature(
            city_id=city.id,
            date_time=current_temperature["date_time"],
            temperature=current_temperature["temperature"],
        )
        db.add(db_temperature)
        temperatures.append(db_temperature)

    db.commit()
    for temperature in temperatures:
        db.refresh(temperature)

    return temperatures


@app.get("/temperatures", response_model=list[schemas.Temperature])
def get_temperatures(city_id: int | None = None, db: Session = Depends(get_db)):
    query = db.query(models.Temperature)
    if city_id is not None:
        query = query.filter(models.Temperature.city_id == city_id)
    return query.all()

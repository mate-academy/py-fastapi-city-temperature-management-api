from datetime import datetime

import httpx
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas import City, Temperature
from app import models
from app.database import engine, get_db


app = FastAPI()

models.Base.metadata.create_all(bind=engine)


async def fetch_temperature(city_name: str):
    async with httpx.AsyncClient() as client:
        geo_response = await client.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": city_name, "count": 1}
        )
        geo_data = geo_response.json()

        if not geo_data.get("results"):
            return None

        latitude = geo_data["results"][0]["latitude"]
        longitude = geo_data["results"][0]["longitude"]

        weather_response = await client.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current": "temperature_2m"
            }
        )

        weather_data = weather_response.json()

        return weather_data["current"]["temperature_2m"]


@app.get("/")
def root():
    return {"message": "API is working"}


@app.post("/cities")
def create_city(city: City, db: Session = Depends(get_db)):
    existing_city = db.query(models.City).filter(
        (models.City.id == city.id) | (models.City.name == city.name)
    ).first()

    if existing_city:
        raise HTTPException(status_code=400, detail="City already exists")

    db_city = models.City(
        id=city.id,
        name=city.name,
        additional_info=city.additional_info
    )

    db.add(db_city)
    db.commit()
    db.refresh(db_city)

    return db_city


@app.get("/cities")
def get_cities(db: Session = Depends(get_db)):
    return db.query(models.City).all()


@app.get("/cities/{city_id}")
def get_city(city_id: int, db: Session = Depends(get_db)):
    city = db.query(models.City).filter(models.City.id == city_id).first()

    if city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return city


@app.put("/cities/{city_id}")
def update_city(city_id: int, city: City, db: Session = Depends(get_db)):
    db_city = db.query(models.City).filter(models.City.id == city_id).first()

    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")

    db_city.name = city.name
    db_city.additional_info = city.additional_info

    db.commit()
    db.refresh(db_city)

    return db_city


@app.delete("/cities/{city_id}")
def delete_city(city_id: int, db: Session = Depends(get_db)):
    city = db.query(models.City).filter(models.City.id == city_id).first()

    if city is None:
        raise HTTPException(status_code=404, detail="City not found")

    db.delete(city)
    db.commit()

    return {"message": "City deleted"}


@app.get("/temperature/{latitude}/{longitude}")
async def get_temperature(latitude: float, longitude: float):
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}&longitude={longitude}"
        f"&current=temperature_2m"
    )

    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    data = response.json()
    temperature = data["current"]["temperature_2m"]

    return {"temperature": temperature}


@app.post("/temperatures/update")
async def update_temperatures(db: Session = Depends(get_db)):
    cities = db.query(models.City).all()

    for city in cities:
        temperature = await fetch_temperature(city.name)

        if temperature is not None:
            db_temperature = models.Temperature(
                city_id=city.id,
                date_time=datetime.now(),
                temperature=temperature
            )

            db.add(db_temperature)

    db.commit()

    return {"message": "Temperatures updated"}


@app.get("/temperatures", response_model=list[Temperature])
def get_temperatures(
    city_id: int | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Temperature)

    if city_id is not None:
        query = query.filter(models.Temperature.city_id == city_id)

    return query.all()

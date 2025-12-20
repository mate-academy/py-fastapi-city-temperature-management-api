from typing import Optional, List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, database
import httpx

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.post("/cities", response_model=schemas.City)
def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)):
    db_city = models.City(name=city.name, additional_info=city.additional_info)
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


@app.get("/cities", response_model=List[schemas.City])
def get_cities(db: Session = Depends(get_db)):
    return db.query(models.City).all()


@app.get("/cities/{city_id}", response_model=schemas.City)
def get_city(city_id: int, db: Session = Depends(get_db)):
    city = db.query(models.City).filter(models.City.id == city_id).first()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@app.delete("/cities/{city_id}")
def delete_city(city_id: int, db: Session = Depends(get_db)):
    city = db.query(models.City).filter(models.City.id == city_id).first()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    db.delete(city)
    db.commit()
    return {"message": f"City {city_id} deleted successfully"}


async def fetch_weather(city_name: str):
    async with httpx.AsyncClient() as client:
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1"
        geo_res = await client.get(geo_url)
        results = geo_res.json().get("results")

        if not results: return None

        lat, lon = results[0]["latitude"], results[0]["longitude"]
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        weather_res = await client.get(weather_url)
        return weather_res.json()["current_weather"]["temperature"]


@app.post("/temperatures/update")
async def update_temperatures(db: Session = Depends(get_db)):
    cities = db.query(models.City).all()
    if not cities:
        return {"message": "No cities found in database"}

    for city in cities:
        temp_val = await fetch_weather(city.name)
        if temp_val is not None:
            new_temp = models.Temperature(city_id=city.id, temperature=temp_val)
            db.add(new_temp)

    db.commit()
    return {"message": "Temperatures updated for all cities"}


@app.get("/temperatures", response_model=List[schemas.Temperature])
def list_temperatures(city_id: Optional[int] = None, db: Session = Depends(get_db)):
    query = db.query(models.Temperature)
    if city_id:
        query = query.filter(models.Temperature.city_id == city_id)
    return query.all()
from typing import Optional

from fastapi.concurrency import run_in_threadpool
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
import httpx
from starlette import status

from . import models, schemas, database


models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="City Temperature API")


# --- City Endpoints ---

@app.post("/cities", response_model=schemas.City)
def create_city(city: schemas.CityCreate, db: Session = Depends(database.get_db)):
    existing_city = db.query(models.City).filter(models.City.name == city.name).first()

    if existing_city:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"City with name '{city.name}' already exists."
        )

    db_city = models.City(name=city.name, additional_info=city.additional_info)
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


@app.get("/cities", response_model=list[schemas.City])
def read_cities(db: Session = Depends(database.get_db)):
    return db.query(models.City).all()


@app.delete("/cities/{city_id}")
def delete_city(city_id: int, db: Session = Depends(database.get_db)):
    city = db.query(models.City).filter(models.City.id == city_id).first()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    db.delete(city)
    db.commit()
    return {"message": "City deleted successfully"}


# --- Temperature Endpoints ---

@app.post("/temperatures/update")
async def update_temperatures(db: Session = Depends(database.get_db)):
    cities = await run_in_threadpool(lambda: db.query(models.City).all())
    if not cities:
        return {"message": "No cities in database"}

    async with httpx.AsyncClient() as client:
        for city in cities:
            try:
                geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city.name}&count=1"
                geo_res = await client.get(geo_url)
                geo_data = geo_res.json().get("results")

                if geo_data:
                    lat, lon = geo_data[0]["latitude"], geo_data[0]["longitude"]

                    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
                    weather_res = await client.get(weather_url)
                    temp = weather_res.json()["current_weather"]["temperature"]

                    new_temp = models.Temperature(
                        city_id=city.id,
                        date_time=datetime.now(),
                        temperature=temp
                    )
                    await run_in_threadpool(db.add, new_temp)
            except Exception as e:
                print(f"Error fetching data for {city.name}: {e}")
                continue

    await run_in_threadpool(db.commit)
    return {"message": f"Temperatures updated for {len(cities)} cities"}


@app.get("/temperatures", response_model=list[schemas.Temperature])
def get_temperatures(city_id: Optional[int] = None, db: Session = Depends(database.get_db)):
    query = db.query(models.Temperature)
    if city_id:
        query = query.filter(models.Temperature.city_id == city_id)
    return query.all()

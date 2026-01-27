from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List
import httpx
import models
import schemas
import database

app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)


@app.post("/cities", response_model=schemas.City)
def create_city(city: schemas.CityCreate, db: Session = Depends(database.get_db)):
    db_city = models.City(**city.model_dump())
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


@app.get("/cities", response_model=List[schemas.City])
def read_cities(db: Session = Depends(database.get_db)):
    return db.query(models.City).all()


@app.delete("/cities/{city_id}")
def delete_city(city_id: int, db: Session = Depends(database.get_db)):
    db_city = db.query(models.City).filter(models.City.id == city_id).first()
    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")
    db.delete(db_city)
    db.commit()
    return {"message": "City deleted"}


@app.post("/temperatures/update")
async def update_temperatures(db: Session = Depends(database.get_db)):
    cities = db.query(models.City).all()
    if not cities:
        return {"message": "No cities in database"}

    async with httpx.AsyncClient() as client:
        for city in cities:
            geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city.name}&count=1"
            geo_res = await client.get(geo_url)
            geo_data = geo_res.json()

            if "results" in geo_data:
                res = geo_data["results"][0]
                lat, lon = res["latitude"], res["longitude"]

                t_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
                t_res = await client.get(t_url)
                t_val = t_res.json()["current_weather"]["temperature"]

                new_temp = models.Temperature(city_id=city.id, temperature=t_val)
                db.add(new_temp)

    db.commit()
    return {"status": "Temperatures updated"}


@app.get("/temperatures", response_model=List[schemas.Temperature])
def get_temperatures(city_id: Optional[int] = None, db: Session = Depends(database.get_db)):
    query = db.query(models.Temperature)
    if city_id:
        query = query.filter(models.Temperature.city_id == city_id)
    return query.all()

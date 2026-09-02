from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import httpx
from typing import List, Optional

import models, schemas
from database import get_db

import logging

logger = logging.getLogger(__name__)

app = FastAPI(title="City Temperature API")


@app.post("/cities", response_model=schemas.City)
def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)):
    db_city = models.City(name=city.name, additional_info=city.additional_info)
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


@app.get("/cities", response_model=List[schemas.City])
def read_cities(db: Session = Depends(get_db)):
    return db.query(models.City).all()


@app.get("/cities/{city_id}", response_model=schemas.City)
def read_city(city_id: int, db: Session = Depends(get_db)):
    city = db.query(models.City).filter(models.City.id == city_id).first()
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@app.put("/cities/{city_id}", response_model=schemas.City)
def update_city(city_id: int, city_update: schemas.CityCreate, db: Session = Depends(get_db)):
    city = db.query(models.City).filter(models.City.id == city_id).first()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    city.name = city_update.name
    city.additional_info = city_update.additional_info
    db.commit()
    db.refresh(city)
    return city


@app.delete("/cities/{city_id}")
def delete_city(city_id: int, db: Session = Depends(get_db)):
    city = db.query(models.City).filter(models.City.id == city_id).first()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    db.delete(city)
    db.commit()
    return {"detail": "City deleted"}


@app.post("/temperatures/update")
async def update_temperatures(db: Session = Depends(get_db)):
    cities = db.query(models.City).all()
    if not cities:
        raise HTTPException(status_code=400, detail="No cities in database to update.")

    updated_records = 0
    failed_cities = []

    async with httpx.AsyncClient() as client:
        for city in cities:
            try:
                response = await client.get(f"https://wttr.in/{city.name}?format=j1", timeout=10.0)
                if response.status_code == 200:
                    data = response.json()
                    temp_c = float(data['current_condition'][0]['temp_C'])

                    new_temp = models.Temperature(city_id=city.id, temperature=temp_c)
                    db.add(new_temp)
                    updated_records += 1
                else:
                    failed_cities.append(city.name)
                    logger.warning(f"Failed to fetch data for {city.name}: Status {response.status_code}")

            except Exception as e:
                logger.error(f"Error updating temperature for {city.name}: {e}")
                failed_cities.append(city.name)
                continue

    db.commit()

    return {
        "message": f"Updated temperatures for {updated_records} cities.",
        "failed_updates": failed_cities
    }


@app.get("/temperatures", response_model=List[schemas.Temperature])
def get_temperatures(city_id: Optional[int] = Query(None), db: Session = Depends(get_db)):
    query = db.query(models.Temperature)
    if city_id:
        query = query.filter(models.Temperature.city_id == city_id)
    return query.all()

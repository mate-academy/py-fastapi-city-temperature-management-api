import asyncio
from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.crud import (
    get_cities,
    create_city,
    get_city_by_id,
    update_city,
    delete_city,
    get_temperatures,
    get_temperatures_by_city_id,
    fetch_city_temperature,
)
from api.database import get_db
from api.models import Temperature, City
from api.schemas import CityListSchema, CityCreateSchema, CityUpdateSchema, TemperatureListSchema

router = APIRouter()


@router.get("/cities", response_model=List[CityListSchema])
def list_cities(db: Session = Depends(get_db)):
    return get_cities(db=db)


@router.post("/cities", response_model=CityListSchema)
def post_city(city: CityCreateSchema, db: Session = Depends(get_db)):
    return create_city(city, db=db)


@router.get("/cities/{city_id}", response_model=CityListSchema)
def detail_city(city_id: int, db: Session = Depends(get_db)):
    return get_city_by_id(city_id=city_id, db=db)


@router.put("/cities/{city_id}", response_model=CityListSchema)
def put_city(city_id: int, city: CityUpdateSchema, db: Session = Depends(get_db)):
    return update_city(city_id=city_id, city=city, db=db)


@router.delete("/cities/{city_id}", response_model=CityListSchema)
def destroy_city(city_id: int, db: Session = Depends(get_db)):
    return delete_city(city_id=city_id, db=db)


@router.get("/temperatures", response_model=List[TemperatureListSchema])
def list_temperatures(db: Session = Depends(get_db)):
    return get_temperatures(db=db)


@router.get("/temperatures/{city_id}", response_model=TemperatureListSchema)
def detail_city_temperatures(city_id: int, db: Session = Depends(get_db)):
    return get_temperatures_by_city_id(city_id=city_id, db=db)


@router.post("/temperatures/update", response_model=List[TemperatureListSchema])
async def update_all_temperatures(db: Session = Depends(get_db)):
    cities = db.query(City).all()
    if not cities:
        raise HTTPException(status_code=404, detail="No cities found")
    tasks = [fetch_city_temperature(city.name) for city in cities]
    temperatures_celsius = await asyncio.gather(*tasks)
    temperature_objs = []
    now = datetime.utcnow()
    for city, temp in zip(cities, temperatures_celsius):
        temperature = Temperature(
            city_id=city.id,
            date_time=now,
            temperature=temp
        )
        db.add(temperature)
        temperature_objs.append(temperature)
    db.commit()
    return temperature_objs

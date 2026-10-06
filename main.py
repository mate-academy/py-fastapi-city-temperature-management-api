import asyncio
from datetime import datetime, timezone

import httpx
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import crud
import schemas
from db.engine import SessionLocal
from db.models import DBCity
from db import models
import logging

logger = logging.getLogger(__name__)

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/cities/", response_model=list[schemas.City])
def read_all_cities(db: Session = Depends(get_db)):
    return crud.get_all_citys(db)


@app.get("/temperatures", response_model=list[schemas.Temperature])
def read_all_temperatures(db: Session = Depends(get_db)):
    return db.query(models.DBTemperature).all()



@app.get("/temperatures/", response_model=list[schemas.Temperature])
def read_temperature_by_city(city_id: int | None = None, db: Session = Depends(get_db)):
    return crud.get_all_temperatures_by_id_city(db=db, city_id=city_id)

@app.post("/cities/", response_model=schemas.City)
def create_city(
    city: schemas.CityCreate,
    db: Session = Depends(get_db)
) -> DBCity:
    return crud.create_city(db=db, city=city)

@app.delete("/cities/{city_id}", status_code=204)
def delete_city(city_id: int, db: Session = Depends(get_db)):
    crud.delete_city(db=db, city_id=city_id)


@app.post("/temperatures/update/")
async def update_temps(db: Session = Depends(get_db)):
    cities = db.query(models.DBCity).all()
    now = datetime.now(timezone.utc)

    async with httpx.AsyncClient() as client:
        tasks = [crud.fetch_city_temp(client, city.name) for city in cities]
        results = await asyncio.gather(*tasks, return_exceptions=True)

    updated = 0
    for city, temp in zip(cities, results):
        if temp is None or isinstance(temp, Exception):
            logger.warning("skip %s: %r", city.name, temp)
            continue

        temp_rec = models.DBTemperature(
            city_id=city.id,
            date_time=now,
            temperature=temp,
        )
        db.add(temp_rec)
        updated += 1

    db.commit()
    return {"updated": updated, "total": len(cities)}

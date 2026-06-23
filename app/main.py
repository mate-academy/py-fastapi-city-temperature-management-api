from datetime import datetime
from typing import List, Optional

import httpx
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import SessionLocal, engine

app = FastAPI()
models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_http_client():
    http_client = httpx.AsyncClient()
    try:
        yield http_client
    finally:
        await http_client.aclose()


@app.get("/")
def read_root():
    return {"Hello2133  ": "World1"}


@app.post("/cities/", response_model=schemas.CityResponse)
def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)):
    city = models.City(
        name=city.name,
        additional_info=city.additional_info,
    )
    db.add(city)
    db.commit()
    db.refresh(city)
    return city


@app.get("/cities/", response_model=List[schemas.CityResponse])
def read_cities(db: Session = Depends(get_db)):
    return db.query(models.City).all()


@app.get("/cities/{city_id}", response_model=schemas.CityResponse)
def get_city(city_id: int, db: Session = Depends(get_db)):
    city = db.query(models.City).filter(models.City.id == city_id).first()

    if city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return city


@app.put("/cities/{city_id}", response_model=schemas.CityResponse)
def update_city(
    city_id: int, city_data: schemas.CityCreate, db: Session = Depends(get_db)
):
    city = db.query(models.City).filter(models.City.id == city_id).first()

    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    city.name = city_data.name
    city.additional_info = city_data.additional_info
    db.commit()
    db.refresh(city)
    return city


@app.delete("/cities/{city_id}", status_code=204)
def delete_city(city_id: int, db: Session = Depends(get_db)):
    city = db.query(models.City).filter(models.City.id == city_id).first()

    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    db.delete(city)
    db.commit()


@app.post("/temperatures/update",
          response_model=schemas.TemperatureUpdateResponse)
async def update_temperatures(
    db: Session = Depends(get_db),
        client: httpx.AsyncClient = Depends(get_http_client)
):
    cities = db.query(models.City).all()
    success_cities = []
    failed_cities = []
    for city in cities:
        query = f"https://wttr.in/{city.name}?format=%t"
        try:
            response = await client.get(query)
            response.raise_for_status()
        except httpx.HTTPError as e:
            failed_cities.append({"city": city.name, "error": str(e)})
            continue
        else:
            clean_text = (
                response.text
                .replace("°C", "")
                .replace("+", "")
                .strip()
            )
            try:
                float_temperature = float(clean_text)
            except ValueError:
                failed_cities.append({
                    "city": city.name,
                    "error": f"Failed to parse temperature value: "
                             f"'{clean_text}'"
                })
                continue

            temperature = models.Temperature(
                city_id=city.id,
                date_time=datetime.now(),
                temperature=float_temperature,
            )
            db.add(temperature)
            success_cities.append({"city": city.name,
                                   "temperature": float_temperature})

    db.commit()
    return {"success_cities": success_cities, "failed_cities": failed_cities}


@app.get("/temperatures/", response_model=List[schemas.TemperatureResponse])
async def get_temperatures(
    db: Session = Depends(get_db), city_id: Optional[int] = None
):
    if city_id is not None:
        temperatures = (
            db.query(models.Temperature)
            .filter(models.Temperature.city_id == city_id)
            .all()
        )
    else:
        temperatures = db.query(models.Temperature).all()
    if not temperatures:
        raise HTTPException(status_code=404, detail="Temperatures not found")
    return temperatures

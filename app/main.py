from datetime import datetime
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

import httpx
from fastapi import Depends, FastAPI, HTTPException, Query, Response, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models import City, Temperature
from app.schemas import CityCreate, CityRead, CityUpdate, TemperatureRead

Base.metadata.create_all(bind=engine)


def seed_demo_data() -> None:
    db = next(get_db())
    try:
        demo_cities = (
            ("Kyiv", "Ukraine"),
            ("Lviv", "Ukraine"),
            ("Odesa", "Ukraine"),
        )
        for name, info in demo_cities:
            if db.query(City).filter(City.name == name).first() is None:
                db.add(City(name=name, additional_info=info))
        db.commit()
    finally:
        db.close()


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    seed_demo_data()
    yield


app = FastAPI(title="City Temperature API", lifespan=lifespan)


@app.post("/cities", response_model=CityRead, status_code=status.HTTP_201_CREATED)
def create_city(city: CityCreate, db: Session = Depends(get_db)) -> City:
    record = City(**city.model_dump())
    db.add(record)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=409, detail="City name already exists") from exc
    db.refresh(record)
    return record


@app.get("/cities", response_model=list[CityRead])
def list_cities(db: Session = Depends(get_db)) -> list[City]:
    return db.query(City).order_by(City.id).all()


@app.get("/cities/{city_id}", response_model=CityRead)
def get_city(city_id: int, db: Session = Depends(get_db)) -> City:
    city = db.get(City, city_id)
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@app.put("/cities/{city_id}", response_model=CityRead)
def update_city(city_id: int, changes: CityUpdate, db: Session = Depends(get_db)) -> City:
    city = db.get(City, city_id)
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    for field, value in changes.model_dump(exclude_unset=True).items():
        setattr(city, field, value)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=409, detail="City name already exists") from exc
    db.refresh(city)
    return city


@app.delete("/cities/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_city(city_id: int, db: Session = Depends(get_db)) -> Response:
    city = db.get(City, city_id)
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    db.delete(city)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.post("/temperatures/update")
async def update_temperatures(db: Session = Depends(get_db)) -> dict[str, int]:
    cities = db.query(City).order_by(City.id).all()
    records: list[Temperature] = []
    async with httpx.AsyncClient(timeout=10.0) as client:
        for city in cities:
            try:
                response = await client.get(
                    "https://geocoding-api.open-meteo.com/v1/search",
                    params={"name": city.name, "count": 1, "language": "en", "format": "json"},
                )
                response.raise_for_status()
                locations = response.json().get("results", [])
                if not locations:
                    continue
                location = locations[0]
                weather_response = await client.get(
                    "https://api.open-meteo.com/v1/forecast",
                    params={
                        "latitude": location["latitude"],
                        "longitude": location["longitude"],
                        "current": "temperature_2m",
                    },
                )
                weather_response.raise_for_status()
                current = weather_response.json()["current"]
                records.append(
                    Temperature(
                        city_id=city.id,
                        date_time=datetime.fromisoformat(current["time"]),
                        temperature=current["temperature_2m"],
                    )
                )
            except (httpx.HTTPError, KeyError, ValueError, TypeError):
                continue
    db.add_all(records)
    db.commit()
    return {"updated": len(records)}


@app.get("/temperatures", response_model=list[TemperatureRead])
def list_temperatures(
    city_id: int | None = Query(default=None), db: Session = Depends(get_db)
) -> list[Temperature]:
    query = db.query(Temperature)
    if city_id is not None:
        query = query.filter(Temperature.city_id == city_id)
    return query.order_by(Temperature.date_time.desc(), Temperature.id.desc()).all()

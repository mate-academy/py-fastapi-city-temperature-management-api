from __future__ import annotations

import asyncio
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.database import SessionLocal, engine
from app.services.open_meteo import fetch_current_temperature, geocode_city

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="City & Temperature API")


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------- City CRUD --------------------
@app.post("/cities", response_model=schemas.CityRead, status_code=status.HTTP_201_CREATED)
def create_city(city_in: schemas.CityCreate, db: Session = Depends(get_db)):
    if crud.get_city_by_name(db, city_in.name) is not None:
        raise HTTPException(status_code=400, detail="City with this name already exists.")
    return crud.create_city(db, city_in)


@app.get("/cities", response_model=list[schemas.CityRead])
def list_cities(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    return crud.get_cities(db, skip=skip, limit=limit)


@app.get("/cities/{city_id}", response_model=schemas.CityRead)
def get_city(city_id: int, db: Session = Depends(get_db)):
    city = crud.get_city(db, city_id)
    if city is None:
        raise HTTPException(status_code=404, detail="City not found.")
    return city


@app.put("/cities/{city_id}", response_model=schemas.CityRead)
def update_city(city_id: int, patch: schemas.CityUpdate, db: Session = Depends(get_db)):
    city = crud.get_city(db, city_id)
    if city is None:
        raise HTTPException(status_code=404, detail="City not found.")
    if patch.name is not None:
        existing = crud.get_city_by_name(db, patch.name)
        if existing is not None and existing.id != city_id:
            raise HTTPException(status_code=400, detail="City with this name already exists.")
    return crud.update_city(db, city, patch)


@app.delete("/cities/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_city(city_id: int, db: Session = Depends(get_db)):
    city = crud.get_city(db, city_id)
    if city is None:
        raise HTTPException(status_code=404, detail="City not found.")
    crud.delete_city(db, city)
    return None


# -------------------- Temperatures --------------------
@app.get("/temperatures", response_model=list[schemas.TemperatureRead])
def list_temperatures(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    city_id: Optional[int] = Query(default=None, ge=1),
    db: Session = Depends(get_db),
):
    return crud.get_temperatures(db, skip=skip, limit=limit, city_id=city_id)


@app.post("/temperatures/update", response_model=schemas.TemperatureUpdateResult)
async def update_temperatures(db: Session = Depends(get_db)):
    cities = crud.get_cities(db, skip=0, limit=500)

    async def process_city(city: models.City) -> dict:
        # Return a detail dict for reporting
        coords = await geocode_city(city.name)
        if coords is None:
            return {"city_id": city.id, "city": city.name, "status": "failed", "reason": "geocoding_not_found"}

        lat, lon = coords
        try:
            temp = await fetch_current_temperature(lat, lon)
        except Exception as exc:  # network/API issues
            return {"city_id": city.id, "city": city.name, "status": "failed", "reason": f"weather_error: {exc}"}

        # DB write (sync) – OK inside async endpoint for small loads
        crud.create_temperature(db, city_id=city.id, temperature_value=temp)
        return {"city_id": city.id, "city": city.name, "status": "ok", "temperature": temp}

    # Fetch in parallel
    results = await asyncio.gather(*(process_city(c) for c in cities))

    created = sum(1 for r in results if r["status"] == "ok")
    failed = len(results) - created

    return schemas.TemperatureUpdateResult(created=created, failed=failed, details=results)

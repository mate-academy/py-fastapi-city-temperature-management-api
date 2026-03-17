import datetime

from fastapi import Depends, FastAPI, HTTPException
import httpx
from starlette.concurrency import run_in_threadpool
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import SessionLocal, engine
from temperature_client import fetch_current_temperature

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="City Temperature Management API")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/cities", response_model=schemas.City)
def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_city(db=db, city=city)
    except IntegrityError as exc:
        raise HTTPException(status_code=400, detail="City name must be unique") from exc


@app.get("/cities", response_model=list[schemas.City])
def list_cities(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_cities(db=db, skip=skip, limit=limit)


@app.get("/cities/{city_id}", response_model=schemas.City)
def get_city(city_id: int, db: Session = Depends(get_db)):
    city = crud.get_city(db=db, city_id=city_id)
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@app.put("/cities/{city_id}", response_model=schemas.City)
def update_city(
    city_id: int, patch: schemas.CityUpdate, db: Session = Depends(get_db)
):
    city = crud.update_city(db=db, city_id=city_id, patch=patch)
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@app.delete("/cities/{city_id}")
def delete_city(city_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_city(db=db, city_id=city_id)
    if not ok:
        raise HTTPException(status_code=404, detail="City not found")
    return {"status": "deleted"}


@app.post("/temperatures/update")
async def update_temperatures(db: Session = Depends(get_db)):
    cities = crud.get_cities(db=db, skip=0, limit=10_000)
    now = datetime.datetime.utcnow()

    created = 0
    failed: list[dict] = []

    for city in cities:
        try:
            temp = await fetch_current_temperature(city.name)
            await run_in_threadpool(
                crud.create_temperature,
                db,
                city.id,
                now,
                temp,
            )
            created += 1
        except (httpx.HTTPError, ValueError) as exc:
            failed.append(
                {
                    "city_id": city.id,
                    "city_name": city.name,
                    "error": str(exc),
                }
            )

    return {"created": created, "failed": failed}


@app.get("/temperatures", response_model=list[schemas.Temperature])
def list_temperatures(
    skip: int = 0,
    limit: int = 100,
    city_id: int | None = None,
    db: Session = Depends(get_db),
):
    return crud.get_temperatures(db=db, skip=skip, limit=limit, city_id=city_id)


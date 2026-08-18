import asyncio
from datetime import datetime, timezone
from typing import AsyncGenerator, Generator, List, Optional

import httpx
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud
import external
import schemas
from database import Base, SessionLocal, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="City Temperature Management API")


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_http_client() -> AsyncGenerator[httpx.AsyncClient, None]:
    async with httpx.AsyncClient(timeout=10.0) as client:
        yield client


@app.post("/cities", response_model=schemas.City, status_code=201)
def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)):
    if crud.get_city_by_name(db, name=city.name) is not None:
        raise HTTPException(
            status_code=400, detail="City with this name already exists"
        )
    return crud.create_city(db, city=city)


@app.get("/cities", response_model=List[schemas.City])
def read_cities(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_cities(db, skip=skip, limit=limit)


@app.get("/cities/{city_id}", response_model=schemas.City)
def read_city(city_id: int, db: Session = Depends(get_db)):
    db_city = crud.get_city(db, city_id=city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city


@app.put("/cities/{city_id}", response_model=schemas.City)
def update_city(
    city_id: int, city: schemas.CityUpdate, db: Session = Depends(get_db)
):
    db_city = crud.get_city(db, city_id=city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")

    existing = crud.get_city_by_name(db, name=city.name)
    if existing is not None and existing.id != city_id:
        raise HTTPException(
            status_code=400, detail="City with this name already exists"
        )
    return crud.update_city(db, db_city=db_city, city=city)


@app.delete("/cities/{city_id}", status_code=204)
def delete_city(city_id: int, db: Session = Depends(get_db)):
    db_city = crud.get_city(db, city_id=city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    crud.delete_city(db, db_city=db_city)


@app.post("/temperatures/update", response_model=List[schemas.Temperature])
async def update_temperatures(
    db: Session = Depends(get_db),
    client: httpx.AsyncClient = Depends(get_http_client),
):
    cities = crud.get_cities(db, limit=1000)
    if not cities:
        return []

    results = await asyncio.gather(
        *(external.fetch_current_temperature(client, city.name) for city in cities),
        return_exceptions=True,
    )

    now = datetime.now(timezone.utc)
    created = []
    for city, result in zip(cities, results):
        if isinstance(result, Exception) or result is None:
            continue
        created.append(
            crud.create_temperature(
                db, city_id=city.id, date_time=now, temperature=result
            )
        )
    return created


@app.get("/temperatures", response_model=List[schemas.Temperature])
def read_temperatures(
    skip: int = 0,
    limit: int = 100,
    city_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    return crud.get_temperatures(db, skip=skip, limit=limit, city_id=city_id)

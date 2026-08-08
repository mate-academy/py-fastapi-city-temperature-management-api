from typing import List, Optional
from datetime import datetime
import asyncio
import httpx
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
import crud
from database import engine, Base, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/cities", response_model=schemas.City)
def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)):
    return crud.create_city(db=db, city=city)

@app.get("/cities", response_model=List[schemas.City])
def read_cities(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_cities(db=db, skip=skip, limit=limit)

@app.get("/cities/{city_id}", response_model=schemas.City)
def read_city(city_id: int, db: Session = Depends(get_db)):
    db_city = crud.get_city(db=db, city_id=city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city

@app.put("/cities/{city_id}", response_model=schemas.City)
def update_city(city_id: int, city_update: schemas.CityUpdate, db: Session = Depends(get_db)):
    return crud.update_city(db=db, city_id=city_id, city_update=city_update)

@app.get("/temperatures", response_model=List[schemas.Temperature])
def read_temperatures(city_id: Optional[int] = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_temperatures(db=db, city_id=city_id, skip=skip, limit=limit)

async def fetch_temperature(client: httpx.AsyncClient, city_name: str) -> Optional[float]:
    try:
        url = f"https://api.example.com/weather?q={city_name}"
        response = await client.get(url)
        if response.status_code == 200:
            data = response.json()
            return data.get("temp")
    except Exception:
        pass
    return None

@app.post("/temperatures/update")
async def update_temperatures(db: Session = Depends(get_db)):
    cities = crud.get_cities(db=db, limit=1000)
    now = datetime.utcnow()
    recorded = []

    async with httpx.AsyncClient() as client:
        tasks = [fetch_temperature(client, city.name) for city in cities]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        for city, temp in zip(cities, results):
            if isinstance(temp, (int, float)):
                db_temp = crud.create_temperature(db=db, city_id=city.id, temp=temp, dt=now)
                recorded.append(db_temp)

    return {"updated": len(recorded)}

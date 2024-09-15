import asyncio
from datetime import datetime
from typing import AsyncGenerator

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import Response

from City import crud as city_crud, schemas as city_schemas
from Temperature import crud as temperature_crud, schemas as temperature_schemas
from Temperature.services import fetch_temperature
from database import models
from database.engine import AsyncSessionLocal

app = FastAPI()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


@app.get("/cities/", response_model=list[city_schemas.City])
async def read_cities(db: AsyncSession = Depends(get_db)) -> list[city_schemas.City]:
    return await city_crud.get_all_cities(db=db)


@app.post("/cities/", response_model=city_schemas.City, status_code=201)
async def create_city(
    city: city_schemas.CityCreate, db: AsyncSession = Depends(get_db)
) -> city_schemas.City:
    return await city_crud.create_city(db=db, city=city)


@app.get("/cities/{city_id}", response_model=city_schemas.City)
async def read_city(city_id: int, db: AsyncSession = Depends(get_db)) -> city_schemas.City:
    return await city_crud.get_city_by_id(db=db, city_id=city_id)


@app.put("/cities/{city_id}", response_model=city_schemas.City)
async def update_city(
    city_id: int, city: city_schemas.CityCreate, db: AsyncSession = Depends(get_db)
) -> city_schemas.City:
    db_city = await city_crud.get_city_by_id(db=db, city_id=city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return await city_crud.update_city(db=db, city_id=city_id, city=city)


@app.delete("/cities/{city_id}", response_model=list[city_schemas.City])
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)) -> Response:
    await city_crud.delete_city(db=db, city_id=city_id)
    return Response(status_code=204)


@app.post("/temperature/update/")
async def update_temperature(db: AsyncSession = Depends(get_db)) -> dict:
    cities = db.query(models.City).all()
    tasks = [fetch_and_store_temperature(db, city) for city in cities]
    await asyncio.gather(*tasks)
    db.commit()
    return {"message": "Temperatures updated successfully"}


async def fetch_and_store_temperature(db: AsyncSession, city: models.City) -> None:
    temperature = await fetch_temperature(city.name)
    temp_record = models.Temperature(
        city_id=city.id, temperature=temperature, date_time=datetime.now()
    )
    db.add(temp_record)


@app.get("/temperatures/", response_model=list[temperature_schemas.Temperature])
async def read_temperatures(
    db: AsyncSession = Depends(get_db),
) -> list[temperature_schemas.Temperature]:
    return await temperature_crud.get_all_temperatures(db=db)


@app.get("/temperatures/{city_id}")
async def get_city_temperatures(
        city_id: int, db: AsyncSession = Depends(get_db)
):
    temperatures = await temperature_crud.get_temperatures_by_city_id(db, city_id)
    if not temperatures:
        raise HTTPException(status_code=404, detail="Temperatures not found")
    return temperatures

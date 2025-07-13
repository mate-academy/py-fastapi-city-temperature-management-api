import asyncio
from contextlib import asynccontextmanager
from http.client import responses

import httpx
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import create_db_and_tables
import city_app.schemas as schemas
import city_app.crud as crud
from dependencies import get_db
import city_app.weather as weather

@asynccontextmanager
async def lifespan(application: FastAPI):
    await create_db_and_tables()
    yield
app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"Hello": "World"}


@app.get("/cities", response_model=list[schemas.CityDto])
async def get_all_cities(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_cities(db)

@app.post("/cities", response_model=schemas.CityDto)
async def create_new_city(city: schemas.CityDtoCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_city(db, city)

@app.delete("/cities/{city_id}")
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.delete_city(db, city_id)


@app.get("/temperatures", response_model=list[schemas.TemperatureDto])
async def get_all_cities(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_temperatures(db)


@app.get("/temperatures/?city_id={city_id}", response_model=list[schemas.TemperatureDto])
async def get_all_cities(city_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.get_temperature_by_city(db, city_id)


@app.post("/temperatures/update", response_model=list[schemas.TemperatureDto])
async def get_all_cities(db: AsyncSession = Depends(get_db)):
    cities = await crud.get_all_cities(db)
    async with httpx.AsyncClient() as client:
        new_temperatures = [weather.get_weather(city, client) for city in cities]
        weather_results = await asyncio.gather(*new_temperatures)

    print(weather_results)
    new_temperatures = []
    for result in weather_results:
        new_temperature = await crud.create_temperature(db, result)
        new_temperatures.append(schemas.TemperatureDto(
            id=new_temperature.id,
            temperature=new_temperature.temperature,
            date_time=new_temperature.date_time,
            city=schemas.CityDtoBase(
                name=new_temperature.city.name,
                additional_info=new_temperature.city.additional_info
            )
        ))

    return new_temperatures



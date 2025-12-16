import asyncio
import os
from typing import Annotated, Optional

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, schemas
from app.dependencies import get_db
from app.models import City, Temperature
from app.schemas import CityListSchema, TemperatureListSchema, TemperatureCreateSchema
import httpx


load_dotenv()

router = APIRouter()

API_KEY = os.getenv("API_KEY")

@router.get("/cities", response_model=list[CityListSchema])
async def get_cities(db: Annotated[AsyncSession, Depends(get_db)]):
    return await crud.get_all_cities(db=db)


@router.post("/cities", response_model=CityListSchema)
async def create_cities(
        city: schemas.CityCreateSchema,
        db: Annotated[AsyncSession, Depends(get_db)]) -> CityListSchema:
    city_to_check = await db.scalar(select(City).where(City.name == city.name))
    if city_to_check:
        raise HTTPException(status_code=400, detail="City already exists")
    return await crud.create_city(db=db, city=city)


@router.delete("/cities/{id}")
async def delete_cities(
        city_id: int,
        db: Annotated[AsyncSession, Depends(get_db)]
):
    return await crud.delete_city(db=db, city_id=city_id)


@router.get("/temperatures/", response_model=list[TemperatureListSchema])
async def get_temperature(
        db: Annotated[AsyncSession, Depends(get_db)],
        city_id: Optional[int] = None,
):
    return await crud.get_all_temperatures(db=db, city_id=city_id)


@router.post("/temperatures/update")
async def update_temperature(db: Annotated[AsyncSession, Depends(get_db)]):
    async with db.begin():
        cities = await crud.get_all_cities(db=db)
        async with httpx.AsyncClient() as client:
            tasks = [client.get(f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city.name}&aqi=no") for city in cities]
            results = await asyncio.gather(*tasks)

            for city, response in zip(cities, results):
                try:
                    if response.is_error:
                        print(f"Problem with updating temperature for {city.name}")
                        continue

                    response = response.json()

                    schema = TemperatureCreateSchema(
                        date_time=response["current"]["last_updated"],
                        temperature=response["current"]["temp_c"],
                        city_id=city.id
                    )

                    await crud.create_temperature(db=db, temperature=schema)

                except Exception as e:
                    print(f"problem with parsing temperature for {city.name}: {e}")

    return {"message": "Temperature successfully updated"}

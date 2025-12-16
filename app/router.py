import os
from typing import Annotated

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


@router.get("/temperatures", response_model=list[TemperatureListSchema])
async def get_temperature(db: Annotated[AsyncSession, Depends(get_db)]):
    return await crud.get_all_temperatures(db=db)


@router.get("/temperatures/?city_id={city_id}", response_model=list[TemperatureListSchema])
async def get_temperature_with_param(
        city_id: int,
        db: Annotated[AsyncSession, Depends(get_db)]
):
    return await crud.get_all_temperatures(db=db, city_id=city_id)


@router.put("/temperatures/update")
async def update_temperature(db: Annotated[AsyncSession, Depends(get_db)]):
    async with db.begin():
        cities = await crud.get_all_cities(db=db)
        async with httpx.AsyncClient() as client:
            for city in cities:
                url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city.name}&aqi=no"
                response = await client.get(url)
                response = response.json()

                temperature = await db.scalar(select(Temperature).where(Temperature.city_id == city.id))

                schema = TemperatureCreateSchema(
                    date_time=response["current"]["last_updated"],
                    temperature=response["current"]["temp_c"],
                    city_id=city.id
                )

                if not temperature:
                    await crud.create_temperature(db=db, temperature=schema)

                else:
                    await crud.update_temperature(db=db, temperature=schema)

    return {"message": "Temperature successfully updated"}

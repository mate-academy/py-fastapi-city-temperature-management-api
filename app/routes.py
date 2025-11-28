import os
from datetime import datetime

import httpx
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db
from app.models import CityModel, TemperatureModel
from app.schemas import CityBase, CityBaseCreate, CityUpdate, TemperatureBase, TemperatureCreate

router = APIRouter()

load_dotenv()

api_key = os.getenv("WEATHER_API_KEY")


@router.get("/cities/", response_model=list[CityBase])
async def get_cities(
        db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(CityModel))
    return result.scalars().all()


@router.get("/cities/{city_id}", response_model=CityBase)
async def get_city(
        city_id: int,
        db: AsyncSession = Depends(get_db),
):
    stmt = select(CityModel).where(CityModel.id == city_id)
    result = await db.execute(stmt)
    city = result.scalars().one_or_none()

    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    return city


@router.post("/cities/", response_model=CityBase)
async def create_city(
        city_data: CityBaseCreate,
        db: AsyncSession = Depends(get_db),
):
    city = CityModel(
        name=city_data.name,
        additional_info=city_data.additional_info,
    )
    db.add(city)
    await db.commit()
    await db.refresh(city)
    return city


@router.patch("/cities/{city_id}")
async def update_city(
        city_data: CityUpdate,
        city_id: int,
        db: AsyncSession = Depends(get_db),
):
    stmt = select(CityModel).where(CityModel.id == city_id)
    result = await db.execute(stmt)
    city = result.scalars().one_or_none()

    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    for field, value in city_data.model_dump(exclude_unset=True).items():
        setattr(city, field, value)

    await db.commit()
    await db.refresh(city)

    return {"detail": "City updated"}


@router.delete("/cities/{city_id}")
async def delete_city(
        city_id: int,
        db: AsyncSession = Depends(get_db),
):
    stmt = select(CityModel).where(CityModel.id == city_id)
    result = await db.execute(stmt)
    city = result.scalars().one_or_none()

    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    await db.delete(city)
    await db.commit()
    return {"detail": "City deleted"}


@router.get("/temperatures/", response_model=list[TemperatureBase])
async def get_temperature(
        city_id: int | None = None,
        db: AsyncSession = Depends(get_db),
):
    query = select(TemperatureModel)

    if city_id is not None:
        query = query.where(TemperatureModel.city_id == city_id)

    result = await db.execute(query)
    return result.scalars().all()


@router.get("/temperatures/{temperature_id}", response_model=TemperatureBase)
async def get_temperature_by_id(
        temperature_id: int,
        db: AsyncSession = Depends(get_db),
):
    stmt = select(TemperatureModel).where(TemperatureModel.id == temperature_id)
    result = await db.execute(stmt)
    temperature = result.scalars().one_or_none()
    if not temperature:
        raise HTTPException(status_code=404, detail="Temperature not found")
    return temperature


@router.post("/temperatures/", response_model=TemperatureBase)
async def create_temperature(
        temperature_data: TemperatureCreate,
        db: AsyncSession = Depends(get_db),
):
    temperature = TemperatureModel(
        city_id=temperature_data.city_id,
        date_time=temperature_data.date_time,
        temperature=temperature_data.temperature,
    )
    db.add(temperature)
    await db.commit()
    await db.refresh(temperature)
    return temperature


@router.post("/temperatures/update/")
async def update_temperature(
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(CityModel))
    cities = result.scalars().all()

    async with httpx.AsyncClient() as client:
        for city in cities:
            try:
                url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city.name}"
                response = await client.get(url)
                data = response.json()
                temperature = data["current"]["temp_c"]
                temperature_record = TemperatureModel(
                    city_id=city.id,
                    date_time=datetime.utcnow(),
                    temperature=temperature,
                )
                db.add(temperature_record)
            except HTTPException as e:
                print (f"error: {e}")

    await db.commit()

    return {"detail": "Temperature updated"}

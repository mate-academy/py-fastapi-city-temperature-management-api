import asyncio
import copy
import os
from datetime import datetime

import httpx
from dotenv import load_dotenv

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from city_api.database import get_db
from city_api.models import City, Temperature
from city_api.schemas import CityCreateResponseSchema, CityCreateRequest, TemperatureResponse


load_dotenv()
router = APIRouter(prefix="/cities")
API_KEY = os.getenv("API_KEY")


async def update_temp(city: City):
    url = "http://api.weatherapi.com/v1/current.json"
    params = {
        "key": API_KEY,
        "q": city.name
    }
    async with httpx.AsyncClient(timeout=5.0) as client:
        try:
            res = await client.get(url=url, params=params)
            response = res.json()
            print(response)
            last_updated_str = response["current"]["last_updated"]
            last_updated = datetime.strptime(last_updated_str, "%Y-%m-%d %H:%M")

            return {
                "city_id": city.id,
                "temp": response["current"]["temp_c"],
                "date_time": last_updated
            }

        except Exception as e:
            print(f"Exception for {city.name}: {e}")
            return None


@router.get("/", response_model = list[CityCreateResponseSchema], tags=["city"])
async def list_cities(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(City))
    cities = result.scalars().all()
    if not cities:
        raise HTTPException(status_code=404, detail="Cities not found.")
    return cities


@router.get("/{city_id}/", response_model=CityCreateResponseSchema, tags=["city"])
async def city_retrieve(city_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(City).filter(City.id == city_id))
    city = result.scalar_one_or_none()

    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    return city


@router.put("/{city_id}/", response_model=CityCreateResponseSchema, tags=["city"])
async def city_update(city_id: int, new_data: CityCreateRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(City).filter(City.id == city_id))
    city = result.scalar_one_or_none()

    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    city.name = new_data.name
    city.additional_info = new_data.additional_info

    db.add(city)
    await db.commit()
    await db.refresh(city)

    return city


@router.post("/", response_model=CityCreateResponseSchema, tags=["city"])
async def create_city(city_data: CityCreateRequest, db: AsyncSession = Depends(get_db)):
    try:
        new_city = City(name=city_data.name, additional_info=city_data.additional_info)
        db.add(new_city)
        await db.commit()
        await db.refresh(new_city)
        new_temperature = Temperature(city_id=new_city.id, temperature=0.0)
        db.add(new_temperature)
        await db.commit()
        return new_city

    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Something went wrong during city creation. ({error})")


@router.delete("/{city_id}/", status_code=200, tags=["city"])
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(City).filter(City.id == city_id))
    city = result.scalar_one_or_none()

    if city:
        await db.delete(city)
        await db.commit()
        return {"msg": "City was deleted successfully"}

    raise HTTPException(status_code=400, detail="City with provided id not exists.")


@router.post("/temperature/update/")
async def update_temperature(db: AsyncSession = Depends(get_db)):
    result_cities = await db.execute(select(City))
    cities = result_cities.scalars().all()

    if not cities:
        raise HTTPException(status_code=404, detail="No cities found.")
    try:
        tasks = []

        for city in cities:
            task = asyncio.create_task(update_temp(city))
            tasks.append(task)

        list_of_changes = await asyncio.gather(*tasks)

        list_of_changes = [change for change in list_of_changes if change is not None]

        if list_of_changes:
            result_temperature = await db.execute(select(Temperature))
            temperatures = result_temperature.scalars().all()

            old_temperature = copy.deepcopy(temperatures)

            for change in list_of_changes:
                for temperature in temperatures:
                    if temperature.city_id == change["city_id"]:
                        temperature.temperature = change["temp"]
                        temperature.date_time = change["date_time"]
                        db.add(temperature)

            await db.commit()

            result = await db.execute(select(Temperature))
            new_cities = result.scalars().all()

            return [
                {
                    "were": old_temperature
                },
                {
                    "got": new_cities
                }
            ]

    except Exception as e:
        return {"msg": f"something went wrong. {e}"}


@router.get("/temperature/", response_model=list[TemperatureResponse], tags=["temperature"])
async def list_temperature(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Temperature))
    temperatures = result.scalars().all()

    if not temperatures:
        raise HTTPException(status_code=404, detail="No temperature records found")

    print(temperatures)
    return temperatures


@router.get("/temperature/{city_id}/", response_model=TemperatureResponse, tags=["temperature"])
async def temperature_retrieve(city_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Temperature).filter(Temperature.city_id == city_id))
    temperature = result.scalar_one_or_none()

    if not temperature:
        raise HTTPException(status_code=404, detail="Not city with given id")

    return temperature




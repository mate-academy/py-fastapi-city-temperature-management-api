import httpx
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app import crud
from app.models import Temperature
from app.schemas import TemperatureOut
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("WEATHER_API_KEY")

router = APIRouter()


async def get_temperature(city_name: str):
    url = f"https://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city_name}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()
        temperature = data["current"]["temp_c"]
        return temperature


@router.get("/temperatures", response_model=list[TemperatureOut])
async def get_temperatures(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Temperature))
    temperatures = result.scalars().all()
    return temperatures


@router.get("/temperatures/{city_id}", response_model=list[TemperatureOut])
async def get_temperatures_by_city(city_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Temperature).filter(Temperature.city_id == city_id))
    temperatures = result.scalars().all()
    return temperatures


@router.post("/temperatures/update")
async def update_temperatures(db: AsyncSession = Depends(get_db)):
    cities = await crud.get_cities(db)

    for city in cities:
        temperature = await get_temperature(city.name)

        await crud.create_temperature(db, city.id, temperature)

    return {"message": "Temperatures updated"}


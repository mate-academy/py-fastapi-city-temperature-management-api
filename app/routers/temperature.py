from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import AsyncSessionLocal
from app.models.city import City
from app.schemas.temperature import TemperatureOut
from app.crud import temperature as crud_temp
import httpx
from app.crud.city import get_cities

router = APIRouter(prefix="/temperatures", tags=["Temperatures"])

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

async def get_city_coordinates(city_name: str):
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        data = resp.json()
        if "results" in data:
            return data["results"][0]["latitude"], data["results"][0]["longitude"]
        return None, None

async def fetch_current_temperature(lat: float, lon: float):
    url = (
        f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
        "&current_weather=true"
    )
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        data = resp.json()
        return data.get("current_weather", {}).get("temperature")

@router.post("/update")
async def update_temperatures(db: AsyncSession = Depends(get_db)):
    cities = await get_cities(db)
    for city in cities:
        lat, lon = await get_city_coordinates(city.name)
        if lat is None:
            continue
        temp = await fetch_current_temperature(lat, lon)
        if temp is not None:
            await crud_temp.create_temperature(db, city.id, temp)
    return {"detail": "Temperatures updated"}

@router.get("/", response_model=list[TemperatureOut])
async def list_temperatures(
    city_id: int = Query(default=None), db: AsyncSession = Depends(get_db)
):
    if city_id is not None:
        return await crud_temp.get_city_temperatures(db, city_id)
    return await crud_temp.get_all_temperatures(db)

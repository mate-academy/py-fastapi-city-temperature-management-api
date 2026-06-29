import os
from datetime import datetime
import httpx
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models import City, Temperature
from app.schemas import TemperatureRead
from dotenv import load_dotenv

load_dotenv()
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
WEATHER_URL = "https://api.weatherapi.com/v1/current.json"

router = APIRouter(prefix="/temperatures", tags=["Temperatures"])


@router.post("/update", status_code=200)
async def update_temperatures(db: AsyncSession = Depends(get_db)):
    cities = (await db.execute(select(City))).scalars().all()
    if not cities:
        raise HTTPException(status_code=404, detail="No cities in database")

    results = []
    async with httpx.AsyncClient() as client:
        for city in cities:
            try:
                resp = await client.get(
                    WEATHER_URL,
                    params={"key": WEATHER_API_KEY, "q": city.name},
                    timeout=10,
                )
                resp.raise_for_status()
                temp_c = resp.json()["current"]["temp_c"]
            except Exception as e:
                results.append({"city": city.name, "error": str(e)})
                continue

            record = Temperature(
                city_id=city.id,
                date_time=datetime.utcnow(),
                temperature=temp_c,
            )
            db.add(record)
            results.append({"city": city.name, "temperature": temp_c})

    await db.commit()
    return {"updated": results}


@router.get("/", response_model=list[TemperatureRead])
async def list_temperatures(
    city_id: int | None = None, db: AsyncSession = Depends(get_db)
):
    query = select(Temperature)
    if city_id is not None:
        query = query.where(Temperature.city_id == city_id)
    result = await db.execute(query)
    return result.scalars().all()

import os

from datetime import datetime
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from httpx import AsyncClient

from city import crud as city_crud
from dependencies import get_db
from temperature import crud
from temperature.models import DBTemperature
from temperature.schemas import Temperature

router = APIRouter()

load_dotenv()

URL = "https://api.weatherapi.com/v1/current.json"
API_KEY = os.environ["API_KEY"]


@router.get("/temperatures/", response_model=list[Temperature])
async def read_temperature(
        db: AsyncSession = Depends(get_db), city_id: int | None = None
):
    return await crud.get_all_temperatures(
        db=db, city_id=city_id
    )


@router.post("/temperatures/update/")
async def update_temperatures(db: AsyncSession = Depends(get_db)):
    cities = await get_cities_from_database(db)

    async with AsyncClient() as client:
        for city in cities:
            params = {
                "key": API_KEY,
                "q": city.name
            }
            try:
                response = await client.get(URL, params=params)
                if response.status_code == 200:
                    temperature_data = response.json()
                    date_time = datetime.now()
                    temperature = temperature_data["current"]["temp_c"]
                    await db.execute(
                        insert(DBTemperature).values(
                            city_id=city.id,
                            date_time=date_time,
                            temperature=temperature
                        )
                    )
                else:
                    raise HTTPException(
                        status_code=response.status_code,
                        detail="Failed to fetch temperature data"
                    )

            except Exception as e:
                print(f"Failed to fetch temperature for city "
                      f"{city.name}: {str(e)}")

    await db.commit()
    return {"message": "Temperatures updated for all cities"}


async def get_cities_from_database(db: AsyncSession = Depends(get_db)):
    return await city_crud.get_all_city(db=db)

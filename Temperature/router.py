import os
import httpx
from typing import List, Optional

from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession
from dotenv import load_dotenv

from Temperature import crud
from City import crud as city_crud
from Temperature import schemas
from dependencies import get_db


load_dotenv()
router = APIRouter()

WEATHER_API_KEY = os.environ.get("API_KEY")
BASE_URL = os.environ.get("API_BASE_URL")


@router.get("/temperatures/", response_model=List[schemas.RetrieveTemperatureSchema])
async def read_temperatures(
        city_id: Optional[int] = None,
        db: AsyncSession = Depends(get_db)
):
    if city_id:
        return await crud.get_temperatures_by_city(db=db, city_id=city_id)

    return await crud.get_temperatures(db=db)


@router.post("/temperatures/update")
async def update_temperatures(db: AsyncSession = Depends(get_db)):
    cities = await city_crud.get_cities(db)

    if not cities:
        return {"message": "No cities found"}

    async with httpx.AsyncClient() as client:
        for city in cities:
            try:
                response = await client.get(
                    BASE_URL,
                    params={
                        "key": WEATHER_API_KEY,
                        "q": city.name
                    }
                )

                if response.status_code != 200:
                    print(f"Error fetching data for {city.name}: {response.text}")
                    continue

                data = response.json()

                current_temp = int(data["current"]["temp_c"])

                await crud.create_temperature(db=db, city_id=city.id, temp_val=current_temp)

            except Exception as e:
                print(f"Global error for city {city.name}: {e}")

    return {"message": "Temperatures updated successfully"}
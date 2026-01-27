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
from settings import settings

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
        return {"message": "No cities found in database"}

    results = {
        "status": "completed",
        "total_processed": len(cities),
        "updated": [],
        "failed": []
    }

    async with httpx.AsyncClient() as client:
        for city in cities:
            try:
                response = await client.get(
                    settings.API_BASE_URL,
                    params={"key": settings.API_KEY, "q": city.name},
                    timeout=10.0
                )
                response.raise_for_status()
                data = response.json()
                current_temp = int(data["current"]["temp_c"])

                await crud.create_temperature(db=db, city_id=city.id, temp_val=current_temp)

                results["updated"].append(city.name)

            except Exception as e:
                error_msg = f"{type(e).__name__}: {str(e)}"
                results["failed"].append({"city": city.name, "error": error_msg})
                print(f"Error for {city.name}: {error_msg}")

            if not results["updated"] and results["failed"]:
                results["status"] = "failed"

            elif results["failed"]:
                results["status"] = "partial_success"

            return results

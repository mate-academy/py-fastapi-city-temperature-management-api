from datetime import datetime

import httpx
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from app.city import crud as city_crud
from app.temperature import crud as temp_crud, schemas

router = APIRouter()


async def fetch_temperature(city_name: str) -> float:
    url = f"https://wttr.in/{city_name}?format=j1"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, timeout=10)
        if response.status_code != 200:
            raise HTTPException(
                status_code=503,
                detail=f"Could not fetch temperature for {city_name}"
            )
        data = response.json()
        return float(data["current_condition"][0]["temp_C"])


@router.get("/", response_model=list[schemas.TemperatureResponse])
async def get_temperatures(
        db: AsyncSession = Depends(get_db),
        city_id: int | None = None
):
    if city_id is not None:
        city = await city_crud.get_city_by_id(db, city_id)
        if not city:
            raise HTTPException(
                status_code=404,
                detail=f"City with id {city_id} not found"
            )

    temperatures = await temp_crud.get_temperatures(db=db, city_id=city_id)
    if not temperatures:
        raise HTTPException(status_code=404, detail="No temperatures found")
    return temperatures


@router.post("/update")
async def update_temperatures(db: AsyncSession = Depends(get_db)):
    cities = await city_crud.get_cities(db)
    if not cities:
        raise HTTPException(status_code=404, detail="No cities found")

    results = []
    errors = []

    for city in cities:
        city_id = city.id
        city_name = city.name
        try:
            temperature = await fetch_temperature(city_name)
            record = await temp_crud.create_temperature(
                db=db,
                city_id=city_id,
                temperature=temperature,
                date_time=datetime.now(),
            )
            results.append({
                "city": city_name,
                "temperature": temperature,
                "date_time": record.date_time,
            })
        except HTTPException as e:
            errors.append({"city": city_name, "error": e.detail})
        except Exception as e:
            errors.append({"city": city_name, "error": str(e)})

    if not results and errors:
        raise HTTPException(
            status_code=503,
            detail=f"Failed to fetch all temperatures: {errors}"
        )

    return {
        "updated": len(results),
        "results": results,
        "errors": errors or None
    }

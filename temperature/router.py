from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from city.crud import get_all_cities
from tasks import fetch_weather
from temperature import schemas, crud
from dependencies import get_db

router = APIRouter()


@router.get("/temperatures/", response_model=list[schemas.Temperature])
async def read_temperatures(
    db: Annotated[AsyncSession, Depends(get_db)], city_id: int | None = None
):
    return await crud.get_all_temperatures(db=db, city_id=city_id)


@router.post("/temperatures/update/")
async def update_temperatures(db: Annotated[AsyncSession, Depends(get_db)]):
    cities = await get_all_cities(db)
    if not cities:
        raise HTTPException(status_code=400, detail="No cities in database")

    results_count = 0

    for city in cities:
        temp = await fetch_weather(city.name)

        if temp is not None:
            await crud.create_temperature_record(db, city.id, temp)
            results_count += 1

    if results_count > 0:
        await db.commit()
    else:
        raise HTTPException(status_code=500, detail="Failed to fetch any weather data")

    return {"message": f"Updated temperatures for {results_count} cities"}

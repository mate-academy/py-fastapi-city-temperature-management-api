import httpx
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.city.crud import read_all_cities
from src.database.dependencies import get_db
from src.services.weather.interface import WeatherClient
from src.temperature.crud import create_temperature, read_cities_temperatures
from src.temperature.dependencies import get_weather_client
from src.temperature.schemas import TemperatureRead

router = APIRouter()

@router.post("/temperatures/update", status_code=status.HTTP_201_CREATED)
async def update_all_cities_temperature(
        db:AsyncSession = Depends(get_db),
        weather_client: WeatherClient = Depends(get_weather_client)
):
    cities = await read_all_cities(db=db) # list[CityRead]  pydantic schema

    updated = False
    failed = []

    for city in cities:
        try:
            weather_data = await weather_client.get_weather(city.name)
            await create_temperature(
                db=db,
                city_id=city.id,
                temperature_data=weather_data
            )
            updated = True
        except httpx.HTTPStatusError as e:
            failed.append({"city": city.name, "error": str(e)})
    if updated and not failed:
        return {"success": True}

    if updated and failed:
        return JSONResponse(
            status_code=status.HTTP_207_MULTI_STATUS,
            content={
                "partial_success": True, "failed": failed
            },
        )

    raise HTTPException(
        status_code=status.HTTP_424_FAILED_DEPENDENCY,
        detail={"success": False, "failed": failed},
    )

@router.get("/temperatures", response_model=list[TemperatureRead])
async def get_city_temperatures(
        city_id: int | None = None,
        db: AsyncSession = Depends(get_db)
) -> list[TemperatureRead]:
    temperatures = await read_cities_temperatures(db=db, city_id=city_id)
    return [TemperatureRead.model_validate(temp) for temp in temperatures]

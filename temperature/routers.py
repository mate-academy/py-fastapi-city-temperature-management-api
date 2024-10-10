from starlette import status
from city.crud import get_city_by_name
from city.schemas import CityBase
from dependencies import db_dependency
from fastapi import APIRouter, Query
from .crud import (
    get_temperature,
    record_temperature,
    get_all_temperatures,
    get_city_temperature
)
from .schemas import TemperatureRead

temperature_router = APIRouter(
    prefix="/temperatures",
    tags=["temperatures"]
)


@temperature_router.post("/update/", status_code=status.HTTP_200_OK)
async def fetch_city_temperature(db: db_dependency, city_name: str):
    city = await get_city_by_name(db, city_name)

    weather_data = await get_temperature(city_name)
    temp_record = await record_temperature(db, city.id, weather_data["temperature"])
    return [
        TemperatureRead(
            id=temp_record.id,
            city_id=temp_record.city_id,
            city=CityBase(
                name=city.name,
                additional_info=city.additional_info
            ),
            date_time=temp_record.date_time,
            temperature=temp_record.temperature

        )
    ]


@temperature_router.get(
    "",
    status_code=status.HTTP_200_OK
)
async def temperature_list(db: db_dependency, skip: int = 0, limit: int = 10):
    temperatures = await get_all_temperatures(db, skip, limit)
    return [
        TemperatureRead(
            id=temp.id,
            city_id=temp.city_id,
            city=CityBase(
                name=temp.city.name,
                additional_info=temp.city.additional_info
            ),
            date_time=temp.date_time,
            temperature=temp.temperature
        )
        for temp in temperatures
    ]


@temperature_router.get("/", status_code=status.HTTP_200_OK)
async def retrieve_city_temperature(
        db: db_dependency,
        city_id: int = Query(gt=0),
        skip: int = 0,
        limit: int = 10
):
    city_temp = await get_city_temperature(db, city_id, skip, limit)
    return [
        TemperatureRead(
            id=temp.id,
            city_id=temp.city_id,
            city=CityBase(
                name=temp.city.name,
                additional_info=temp.city.additional_info
            ),
            date_time=temp.date_time,
            temperature=temp.temperature
        )
        for temp in city_temp
    ]

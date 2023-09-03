import datetime

import httpx
from fastapi import HTTPException
from sqlalchemy import select, insert, extract
from sqlalchemy.ext.asyncio import AsyncSession

import settings
from city import models as city_models
from temperature import models as temperature_models
from temperature import schemas


async def get_weather_data(
        db: AsyncSession
) -> dict:
    query = select(city_models.DBCity)
    cities_list = await db.execute(query)
    filtering = [
        (city_db[0].name, city_db[0].id) for city_db in cities_list.fetchall()
    ]

    weather_data_for_cities = {}
    for city in filtering:
        params = {"q": city, "key": settings.API_KEY}
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(settings.URL, params=params)
                if response.status_code == 200:
                    weather_data = response.json()
                    weather_data_for_cities[city] = weather_data["current"]["temp_c"]
                else:
                    print(f"API request for {city} failed with status code: {response.status_code}")
        except (TypeError, httpx.RequestError) as e:
            raise HTTPException(
                status_code=400,
                detail=f"Error in API request for {city}: {str(e)}"
            )

    return weather_data_for_cities


async def save_temperature(
        temperature_data: schemas.TemperatureCreate,
        db: AsyncSession
) -> dict:
    weather_data_for_cities = await get_weather_data(db=db)
    for city in weather_data_for_cities:
        temperature_entry = insert(temperature_models.DBTemperature).values(
            city_id=city[1],
            date_time=datetime.datetime.now(),
            temperature=weather_data_for_cities[city],
        )

        await db.execute(temperature_entry)
        await db.commit()
    return {**temperature_data.model_dump()}


async def get_temperatures(
        db: AsyncSession, skip: int = 0, limit: int = 100
) -> list[schemas.Temperature]:
    temperature_query = select(temperature_models.DBTemperature).offset(skip).limit(limit)
    temperature_list = await db.execute(temperature_query)
    return [temperature[0] for temperature in temperature_list.fetchall()]


async def get_temperature_by_city_id(
        city_id: int, db: AsyncSession
) -> list[schemas.Temperature]:
    city = select(temperature_models.DBTemperature).filter(
        temperature_models.DBTemperature.city_id == city_id
    )
    result = await db.execute(city)
    return [temperature[0] for temperature in result.fetchall()]


async def get_temperature_by_date(
        date: str, db: AsyncSession
) -> list[schemas.Temperature]:
    try:
        formatted_date = datetime.datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Date '{date}' does not match the format 'YYYY-MM-DD'"
        )

    temperature = select(temperature_models.DBTemperature).filter(
        extract("year", temperature_models.DBTemperature.date_time) == formatted_date.year,
        extract("month", temperature_models.DBTemperature.date_time) == formatted_date.month,
        extract("day", temperature_models.DBTemperature.date_time) == formatted_date.day
    )
    result = await db.execute(temperature)
    return [temperature[0] for temperature in result.fetchall()]

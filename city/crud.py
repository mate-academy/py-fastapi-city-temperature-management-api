import json
from typing import Any
from datetime import datetime

from fastapi import HTTPException
from requests import Response, request
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from city import models, schemas
from settings import settings


async def get_cities_list(db: AsyncSession) -> list[models.DBCity]:
    query = select(models.DBCity)
    city_list = await db.execute(query)

    return [city[0] for city in city_list.all()]


async def get_city(city_id: int, db: AsyncSession) -> models.DBCity:
    query = select(models.DBCity).filter(models.DBCity.id == city_id)

    db_city = await db.execute(query)
    db_city = db_city.first()

    if db_city is None:
        raise HTTPException(
            status_code=404,
            detail=f"City with id {city_id} not found",
        )

    return db_city[0]


async def create_city(
        city: schemas.CityCreate,
        db: AsyncSession,
) -> dict[str, Any]:
    query = insert(models.DBCity).values(
        name=city.name,
        additional_info=city.additional_info,
    )

    result = await db.execute(query)
    await db.commit()

    response = {**city.model_dump(), "id": result.lastrowid}

    return response


async def update_city(
    city: schemas.CityCreate,
    city_id: int,
    db: AsyncSession
) -> dict[str, Any]:
    query = (
        update(models.DBCity).where(models.DBCity.id == city_id).values(
            name=city.name,
            additional_info=city.additional_info,
        )
    )

    await db.execute(query)
    await db.commit()

    response = {**city.model_dump(), "id": city_id}

    return response


async def delete_city(city_id: int, db: AsyncSession) -> dict[str, str]:
    query = delete(models.DBCity).where(models.DBCity.id == city_id)

    await db.execute(query)
    await db.commit()

    return {"Message": "Item was deleted"}


async def make_weather_api_get_request(city_name: str) -> Response:
    url = (
        f"{settings.temperature_api_url}"
        f"?key={settings.temperature_api_key}&q={city_name}"
    )

    response = request(url=url, method="GET")

    return response


async def decode_response(response: Response) -> dict[str: Any]:
    content_json = json.loads(response.content.decode("utf-8"))
    return content_json


async def get_temperature_from_content(content: dict[str: Any]) -> float:
    temperature_in_celsius = content["current"]["temp_c"]
    return temperature_in_celsius


async def get_new_temperature(city_name: str) -> float:
    response = await make_weather_api_get_request(city_name)
    content = await decode_response(response)
    new_temperature = await get_temperature_from_content(content)

    return new_temperature


async def get_temperatures_list(
        db: AsyncSession,
        city_id: int | None = None
) -> list[schemas.Temperature]:
    query = select(models.DBTemperature)

    if city_id:
        query = query.filter(models.DBTemperature.city_id == city_id)

    temperature_list = await db.execute(query)

    return [temperature[0] for temperature in temperature_list.all()]


async def create_temperature(
    temperature: schemas.TemperatureCreate,
    db: AsyncSession
) -> dict[str, Any]:

    query = insert(models.DBTemperature).values(
        city_id=temperature.city_id,
        temperature=temperature.temperature,
        date_time=temperature.date_time,
    )

    result = await db.execute(query)
    await db.commit()

    response = {**temperature.model_dump(), "id": result.lastrowid}

    return response


async def update_single_temperature(
    temperature_schema: schemas.TemperatureCreate,
    temperature_id: int,
    db: AsyncSession
) -> dict[str, Any]:

    query = (
        update(models.DBTemperature).where(
            models.DBTemperature.id == temperature_id
        ).values(
            temperature=temperature_schema.temperature,
            date_time=temperature_schema.date_time,
        )
    )

    await db.execute(query)
    await db.commit()

    response = {**temperature_schema.model_dump(), "id": temperature_id}

    return response


async def update_temperatures(db: AsyncSession) -> list[schemas.Temperature]:

    city_query = select(models.DBCity)
    cities_list = await db.scalars(city_query)

    current_date_time = datetime.now()

    for city in cities_list.all():
        db_temperature = await city.awaitable_attrs.temperature
        current_temperature = await get_new_temperature(city.name)

        temperature_schema = schemas.TemperatureCreate(
            city_id=city.id,
            date_time=current_date_time,
            temperature=current_temperature
        )

        if db_temperature is None:
            await create_temperature(
                temperature=temperature_schema,
                db=db
            )
        else:
            await update_single_temperature(
                temperature_schema=temperature_schema,
                temperature_id=db_temperature.id,
                db=db
            )

    temperature_query = select(models.DBTemperature)
    temperature_list = await db.execute(temperature_query)

    return [temperature[0] for temperature in temperature_list.all()]

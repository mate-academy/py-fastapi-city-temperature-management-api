import httpx
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from datetime import datetime
from app.schemes.temperature import (
    TemperatureCreate, TemperatureUpdate, TemperatureResponse
)
from app.db.models import CityModel, TemperatureModel
from app.exeptions import CityNotFound, TemperatureNotFound


def create_temperature(
        db: Session,
        data: TemperatureCreate) -> TemperatureResponse:
    if not db.query(CityModel).filter(CityModel.id == data.city_id).first():
        raise CityNotFound(f"City {data.city_id} not found")

    db_temperature = TemperatureModel(**data.model_dump())
    db.add(db_temperature)
    db.commit()
    db.refresh(db_temperature)
    return TemperatureResponse.model_validate(db_temperature)


def get_all_temperatures(
        db: Session,
        skip: int = 0,
        limit: int = 100) -> list[TemperatureResponse]:
    db_temperatures = (
        db.query(TemperatureModel)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return [
        TemperatureResponse.model_validate(temperature)
        for temperature in db_temperatures
    ]


def get_temperature_by_city_id(
        db: Session,
        city_id: int
) -> list[TemperatureResponse]:
    db_temperatures = (
        db.query(TemperatureModel)
        .filter(TemperatureModel.city_id == city_id)
        .all()
    )
    return [
        TemperatureResponse.model_validate(temperature)
        for temperature in db_temperatures
    ]


def update_temperature(
        db: Session,
        temperature_id: int,
        data: TemperatureUpdate
) -> TemperatureResponse:

    db_temperature = (
        db.query(TemperatureModel)
        .filter(TemperatureModel.id == temperature_id)
        .first()
    )

    if not db_temperature:
        raise TemperatureNotFound(f"Temperature with {temperature_id} not found")

    if data.city_id is not None:
        if not (
                db.query(CityModel)
                .filter(CityModel.id == data.city_id)
                .first()
        ):
            raise CityNotFound(f"City with id {data.city_id} not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(db_temperature, key, value)

    db.add(db_temperature)
    db.commit()
    db.refresh(db_temperature)
    return TemperatureResponse.model_validate(db_temperature)


async def auto_insert_temperature(db: AsyncSession) -> list[TemperatureResponse]:
    cities = await db.scalars(select(CityModel))

    async with httpx.AsyncClient(timeout=10) as client:
        for city in cities:
            try:
                response = await client.get(
                    "https://geocoding-api.open-meteo.com/v1/search",
                    params={"name": city.name, "count": 1},
                )
                response.raise_for_status()
            except httpx.HTTPError as e:
                raise CityNotFound(str(e))

            data = response.json()
            if "results" in data and len(data["results"]) > 0:
                latitude = data["results"][0]["latitude"]
                longitude = data["results"][0]["longitude"]

                try:
                    weather_results = await client.get(
                        "https://api.open-meteo.com/v1/forecast",
                        params={
                            "latitude": latitude,
                            "longitude": longitude,
                            "current": "temperature_2m",
                        },
                    )
                    weather_results.raise_for_status()
                except httpx.HTTPError as e:
                    raise TemperatureNotFound(str(e))

                weather_data = weather_results.json()
                try:
                    temperature_value = weather_data["current"]["temperature_2m"]
                    date_time = datetime.fromisoformat(
                        weather_data["current"]["time"]
                    )
                except (KeyError, TypeError, ValueError) as e:
                    raise TemperatureNotFound(str(e))

                db_temperature = TemperatureModel(
                    city_id=city.id,
                    temperature=temperature_value,
                    date_time=date_time,
                )
                db.add(db_temperature)

                await db.commit()
                await db.refresh(db_temperature)

    db_temperatures = await db.scalars(
        select(TemperatureModel).order_by(TemperatureModel.date_time.desc())
    )
    return [
        TemperatureResponse.model_validate(temperature)
        for temperature in db_temperatures
    ]


def delete_temperature(db: Session, temperature_id: int) -> bool:
    db_temperature = (
        db.query(TemperatureModel)
        .filter(TemperatureModel.id == temperature_id)
        .first()
    )

    if not db_temperature:
        raise TemperatureNotFound(f"Temperature with id {temperature_id} not found")

    db.delete(db_temperature)
    db.commit()

    return True

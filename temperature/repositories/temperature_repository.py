import asyncio

import httpx
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from city.repositories.city_repository import CityRepository
from db import models
from settings import settings
from temperature import schemas
from city import schemas as city_schemas


class TemperatureRepository:
    def __init__(
        self, session: AsyncSession,
        city_repository: CityRepository = None
    ):
        self.session = session
        self.city_repository = city_repository or CityRepository(session)

    async def get_temperatures_list(
        self,
        city_id: int = None
    ) -> list[schemas.Temperature]:
        query = select(models.Temperature)
        if city_id:
            query = query.where(models.Temperature.city_id == city_id)

        temperature_list = await self.session.execute(query)
        return [
            schemas.Temperature.model_validate(temperature[0])
            for temperature in temperature_list.fetchall()
        ]

    async def get_temperature_by_id(
        self,
        temperature_id: int
    ) -> schemas.Temperature:
        query = select(models.Temperature).where(models.Temperature.id == temperature_id)
        result = await self.session.execute(query)
        temperature_db = result.scalar_one_or_none()
        if temperature_db:
            return schemas.Temperature.model_validate(
                temperature_db,
            )

    async def create_temperature(
        self,
        temperature: schemas.TemperatureCreate,
        session: AsyncSession = None
    ) -> models.Temperature:
        if not session:
            session = self.session
        temperature_db = models.Temperature(
            city_id=temperature.city_id,
            temperature=temperature.temperature,
            date_time=temperature.date_time,
        )
        session.add(temperature_db)
        await session.commit()
        await session.refresh(temperature_db)
        return schemas.Temperature.model_validate(
            temperature_db,
        )

    async def _fetch_city_temperature(
        self,
        city: models.City,
        client: httpx.AsyncClient
    ) -> models.Temperature | None:
        response = await client.get(
            settings.WEATHER_API_URL,
            params={"key": settings.API_KEY, "q": city.name},
        )
        json_response = response.json()
        if not json_response.get("current", False):
            # todo create some logs
            return
        temperature_schema = models.Temperature(
            temperature=json_response["current"]["temp_c"],
            city_id=city.id,
            date_time=datetime.now(),
        )
        return temperature_schema

    async def _get_temperatures_from_api(
        self, cities: [city_schemas.City]
    ) -> tuple[models.Temperature]:
        async with httpx.AsyncClient() as client:
            results = await asyncio.gather(
                *[
                    self._fetch_city_temperature(city, client)
                    for city in cities
                ]
            )
        return results

    async def fetch_temperatures_for_all_cities(
        self
    ) -> None:
        async with self.session.begin():
            cities = await self.city_repository.get_cities_list()

            results = await self._get_temperatures_from_api(cities)

            self.session.add_all(
                result for result in results if result
            )

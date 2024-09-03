from typing import (
    Sequence,
    Optional
)

import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app import models, schemas
from app.api import weather


class CityRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> Sequence[models.City]:
        query = select(models.City)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_one(self, city_id: int) -> Optional[models.City]:
        query = select(models.City).where(models.City.id == city_id)
        result = await self.session.execute(query)
        return result.scalars().first()

    async def create(self, city: schemas.City) -> None:
        self.session.add(city)
        await self.session.flush()
        await self.session.refresh(city)

    async def update(self, city: schemas.City) -> None:
        await self.session.flush()
        await self.session.refresh(city)

    async def delete(self, city: schemas.City) -> None:
        await self.session.delete(city)


class TemperatureRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_temperatures(self, city_id: int) -> Sequence[models.Temperature]:
        query = select(models.Temperature)

        if city_id:
            query = query.where(models.Temperature.city_id == city_id)

        result = await self.session.execute(query)
        return result.scalars().all()

    async def create(self, temperature: schemas.Temperature) -> None:
        self.session.add(temperature)
        await self.session.flush()
        await self.session.refresh(temperature)


class Service:
    def __init__(self, session: AsyncSession):
        self.city = CityRepository(session)
        self.temperature = TemperatureRepository(session)

    async def get_cities(self) -> Sequence[schemas.City]:
        cities = await self.city.get_all()
        return [schemas.City.model_validate(city) for city in cities]


    async def get_city(self, city_id: int) -> schemas.City:
        city = await self.city.get_one(city_id)
        return schemas.City.model_validate(city)


    async def create_city(self, city: schemas.CityCreate) -> schemas.City:
        new_city = models.City(
            name=city.name,
            additional_info=city.additional_info
        )
        async with self.city.session.begin():
            await self.city.create(new_city)
        return schemas.City.model_validate(new_city)


    async def update_city(self, city_id: int, city: schemas.CityCreate) -> schemas.City:
        city_to_update = await self.get_city(city_id)

        city_to_update.name = city.name
        city_to_update.additional_info = city.additional_info

        async with self.city.session.begin():
            await self.city.update(city_to_update)

        return schemas.City.model_validate(city_to_update)

    async def delete_city(self, city_id: int) -> schemas.City:
        city_to_delete = await self.get_city(city_id)

        async with self.city.session.begin():
            await self.city.session.delete(city_to_delete)

        return city_to_delete

    async def get_temperatures(self, city_id: int = None) -> Sequence[models.Temperature]:
        temperatures = await self.temperature.get_temperatures(city_id)
        return [schemas.Temperature.model_validate(temp) for temp in temperatures]

    async def create_temperatures(self) -> dict:
        cities = await self.city.get_all()

        async with httpx.AsyncClient() as client:
            for city in cities:
                temperature = await weather.fetch_temperatures(client, city)
                temperature = models.Temperature(**temperature.dict())
                await self.temperature.create(temperature)

        return {
            "detail": "Temperatures successfully updated"
        }

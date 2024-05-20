from datetime import datetime
from sqlalchemy import select
from src.city_weather.db_managers.abstract_manager import AbstractDBManager
from src.city_weather.db_managers.city_manager import CityDBManager
from src.city_weather.models import Temperature
from src.city_weather.weather_api import get_tepmerature
from src.database import SessionLocal


class TemperatureDBManager(AbstractDBManager):
    model = Temperature

    async def update_item(self, city_manager: CityDBManager):
        cities = await city_manager.get_list_of_items()
        for city in cities:
            temperature = await get_tepmerature(city.name)
            if temperature:
                await self.create_new_item(temperature, city.id)

    async def create_new_item(self, temperature: float, city_id: int):
        async with SessionLocal() as session:
            new_item = self.model(city_id=city_id, temperature=temperature, date_time=datetime.now())
            session.add(new_item)
            await session.commit()

    async def get_items_by_city(self, city_id: int):
        async with SessionLocal() as session:
            return await session.scalars(select(self.model).where(self.model.city_id == city_id))

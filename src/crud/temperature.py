from datetime import UTC, datetime

import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.settings import get_settings
from src.models import CityModel, TemperatureModel
from src.schemas.city import CityRequestSchema


class TemperatureService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.settings = get_settings()
        self.api_key = self.settings.WEATHER_API_KEY

    async def fetch_temperature(self, city: CityRequestSchema) -> float:
        try:
            weather_url = "https://api.weatherapi.com/v1/current.json"
            params = {"key": self.api_key, "q": city}
            async with httpx.AsyncClient() as client:
                response = await client.get(weather_url, params=params)
                response.raise_for_status()
                weather_data = response.json()
            current = weather_data["current"]
            temperature = current["temp_c"]
            return temperature
        except Exception:
            await self.db.rollback()
            raise

    async def update_all_cities_temperatures(self) -> None:
        try:
            cities = (await self.db.scalars(select(CityModel))).all()
            for city in cities:
                city_schema = CityRequestSchema(name=city.name)
                temperature = await self.fetch_temperature(city_schema)
                temp_obj = TemperatureModel(
                    city_id=city.id,
                    date_time=datetime.now(UTC),
                    temperature=temperature
                )
                self.db.add(temp_obj)
            await self.db.commit()

        except Exception:
            await self.db.rollback()
            raise

    async def get_temperature(self) -> list[TemperatureModel]:
        result = await self.db.scalars(select(TemperatureModel))
        return list(result.all())

    async def get_temperature_by_city_id(self, city_id: int) -> TemperatureModel | None:
        temperature = await self.db.scalar(select(TemperatureModel).where(TemperatureModel.city_id == city_id))
        return temperature

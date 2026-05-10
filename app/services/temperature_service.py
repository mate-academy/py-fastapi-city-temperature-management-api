from app.repositories.temperature_repository import TemperatureRepository
from app.repositories.city_repository import CityRepository
from app.models.temperature import DBTemperature
from app.services.weather_client import WeatherClient
from datetime import datetime


class TemperatureService:
    def __init__(self, temp_repo: TemperatureRepository,
                 city_repo: CityRepository,
                 weather_client: WeatherClient):
        self.temp_repo = temp_repo
        self.city_repo = city_repo
        self.weather_client = weather_client

    async def update_all_cities_weather(self):
        cities = await self.city_repo.get_all()

        weather_data_list = []
        for city in cities:
            try:
                temp = await self.weather_client.get_current_temp(city.name)

                weather_data_list.append(DBTemperature(
                    city_id=city.id,
                    temperature=temp,
                    date_time=datetime.utcnow()
                ))
            except Exception as e:
                print(f"Can't get weather for {city.name}: {e}")
                continue

        await self.temp_repo.create_many(weather_data_list)

    async def get_all_history(self):
        return await self.temp_repo.get_all()

    async def get_history_by_city(self, city_id: int):
        return await self.temp_repo.get_by_city(city_id)

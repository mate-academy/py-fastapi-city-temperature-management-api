from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.repositories.city_repository import CityRepository
from app.repositories.temperature_repository import TemperatureRepository
from app.services.city_service import CityService
from app.services.temperature_service import TemperatureService
from app.services.weather_client import WeatherClient


def get_city_repository(session: AsyncSession = Depends(get_db)):
    return CityRepository(session)


def get_temperature_repository(session: AsyncSession = Depends(get_db)):
    return TemperatureRepository(session)


def get_weather_client():
    return WeatherClient()


def get_city_service(repo: CityRepository = Depends(get_city_repository)):
    return CityService(repo)


def get_temperature_service(
        temp_repo: TemperatureRepository = Depends(get_temperature_repository),
        city_repo: CityRepository = Depends(get_city_repository),
        weather_client: WeatherClient = Depends(get_weather_client)
):
    return TemperatureService(temp_repo, city_repo, weather_client)

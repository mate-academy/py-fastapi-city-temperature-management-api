from src.city_weather.db_managers.abstract_manager import AbstractDBManager
from src.city_weather.db_managers.city_manager import CityDBManager
from src.city_weather.db_managers.temperature_manager import TemperatureDBManager


def get_city_manager() -> AbstractDBManager:
    return CityDBManager()


def get_temperature_manager() -> AbstractDBManager:
    return TemperatureDBManager()

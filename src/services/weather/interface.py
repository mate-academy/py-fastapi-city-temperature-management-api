from typing import Protocol

from src.services.weather.schemas import WeatherData


class WeatherClient(Protocol):
    async def get_weather(self, city_name: str) -> WeatherData:
        ...
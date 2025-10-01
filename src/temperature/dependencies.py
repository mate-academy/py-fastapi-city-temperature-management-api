from src.services.weather.get_weather import WeatherApiClient
from src.services.weather.interface import WeatherClient

async def get_weather_client() -> WeatherClient:
    return WeatherApiClient()

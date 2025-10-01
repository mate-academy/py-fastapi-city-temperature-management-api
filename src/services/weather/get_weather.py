import httpx
from src.settings import settings
from src.temperature.schemas import WeatherData

# client for WeatherApi https://www.weatherapi.com/

class WeatherApiClient:
    async def get_weather(self, city_name: str) -> WeatherData:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url=settings.WEATHER_API_URL,
                params={"q": city_name, "key": settings.WEATHER_API_KEY}
            )
            response.raise_for_status()
            data = response.json()
            print(data)
            return WeatherData(
                temp_c=data["current"]["temp_c"],
                last_updated=data["current"]["last_updated"]
            )

# client for Open Weather Map https://openweathermap.org/
# class Open_Weather_Map_Client:
#     async def get_weather(self, city_name: str) -> WeatherData:
#         async with httpx.AsyncClient() as client:
#             response = await client.get(
#                 url=settings.Open_Weather_Map_API_URL,
#                 params={
#                     "q": city_name,
#                     "appid": settings.Open_Weather_Map_API_KEY,
#                     "units": "metric"
#                 }
#             )
#             response.raise_for_status()
#             data = response.json()
#             return WeatherData(
#                 temp_c=data["main"]["temp"],
#                 last_updated=data["dt"]
#             )

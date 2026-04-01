import httpx
from db.config import settings


async def get_temperature(city_name: str) -> float | None:
    async with httpx.AsyncClient() as client:
        location_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=5&appid={settings.API_KEY}"
        location_data = await client.get(location_url)
        location = location_data.json()
        try:
            location_lat = location[0]["lat"]
            location_lon = location[0]["lon"]
            weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={location_lat}&lon={location_lon}&appid={settings.API_KEY}"
            weather_data = await client.get(weather_url)
            weather = weather_data.json()
            return round(weather["main"]["temp"] - 273.15, 1)
        except IndexError:
            return None
        except KeyError:
            raise
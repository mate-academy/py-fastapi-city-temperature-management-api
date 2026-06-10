from settings import settings
import httpx


api_key = settings.OPENWEATHER_API_KEY

async def fetch_temperature_by_coordinates(latitude: float, longitude: float) -> float | None:
    async with httpx.AsyncClient() as client:
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "lat": latitude,
            "lon": longitude,
            "appid": api_key,
            "units": "metric",
        }
        response = await client.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            return data["main"]["temp"]
        return None

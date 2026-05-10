import httpx
from app.core.config import settings


class WeatherClient:
    def __init__(self):
        self.api_key = settings.WEATHER_API_KEY
        self.base_url = settings.WEATHER_API_URL

    async def get_current_temp(self, city_name: str) -> float:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                self.base_url,
                params={"key": self.api_key, "q": city_name}
            )
            response.raise_for_status()
            data = response.json()
            return float(data["current"]["temp_c"])

import httpx

WEATHER_API_URL = "https://api.weatherapi.com/v1/current.json"

class WeatherAPI:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    async def get_temperature(self, city: str | None = None) -> float | None:
        async with httpx.AsyncClient() as client:
            params = {"key": self.api_key, "q": city}
            try:
                response = await client.get(WEATHER_API_URL, params=params)
                response.raise_for_status()
                data = response.json()
                return data["current"]["temp_c"]
            except Exception:
                return None

import os
import httpx


API_KEY = os.getenv("WEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
REQUEST_TIMEOUT_SECONDS = 10.0


async def fetch_temperature(city_name: str) -> float | None:
    if not API_KEY:
        return None

    params = {
        "q": city_name,
        "appid": API_KEY,
        "units": "metric"
    }
    async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT_SECONDS) as client:
        try:
            response = await client.get(BASE_URL, params=params)
            if response.status_code == 200:
                data = response.json()
                main_data = data.get("main")
                if isinstance(main_data, dict):
                    temp = main_data.get("temp")
                    if isinstance(temp, int | float):
                        return float(temp)
            else:
                return None
        except (httpx.RequestError, ValueError):
            return None

    return None

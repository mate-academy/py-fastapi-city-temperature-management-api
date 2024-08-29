import httpx

from app.core.config import settings


async def fetch_current_temperature(city_name: str) -> float:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"http://api.weatherapi.com/v1/current.json",
                params={"key": settings.API_KEY, "q": city_name},
            )
            response.raise_for_status()
            data = response.json()
            return data["current"]["temp_c"]
        except httpx.HTTPStatusError as e:
            print(f"Error fetching data for city {city_name}: {str(e)}")
            raise e

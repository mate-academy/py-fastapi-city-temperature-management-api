import asyncio

import aiohttp
from fastapi import HTTPException, status

from app.config.settings import get_settings

settings = get_settings()


class WeatherAPIError(Exception):
    pass


async def get_current_temperature(
    city_name: str, session: aiohttp.ClientSession
) -> float:
    url = f"{settings.weather_api_base_url}/current.json"
    params = {
        "key": settings.weather_api_key,
        "q": city_name,
        "aqi": "no",
    }

    try:
        async with session.get(url, params=params) as response:
            if response.status == status.HTTP_404_NOT_FOUND:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"City '{city_name}' not found",
                )
            data = await response.json()
            return data["current"]["temp_c"]

    except aiohttp.ClientError as error:
        raise WeatherAPIError(f"Error connecting to WeatherAPI: {str(error)}")
    except KeyError as error:
        raise WeatherAPIError(f"Unexpected API response format: {str(error)}")


async def get_current_temperatures(
    city_names: list[str], session: aiohttp.ClientSession
) -> dict[str, float]:

    async def get_temp(city: str) -> tuple[str, float | None]:
        try:
            temp = await get_current_temperature(city, session)
            return city, temp
        except (HTTPException, WeatherAPIError) as error:
            print(f"Error getting temperature for {city}: {str(error)}")
            return city, None

    results = await asyncio.gather(*[get_temp(city) for city in city_names])
    return {city: temp for city, temp in results if temp}

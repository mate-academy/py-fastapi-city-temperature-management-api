from asyncio import gather

from aiohttp import ClientSession

from src.config import settings
from src.exceptions import FetchTemperatureError
from src.temperatures.schemas import TemperatureCreate


async def _fetch_temperature(
    session: ClientSession, city: dict[str, int | str]
) -> TemperatureCreate | FetchTemperatureError:
    params = {"q": city["name"], "key": settings.WEATHERAPI_KEY}
    async with session.get(settings.WEATHER_URL, params=params) as response:
        response_json = await response.json()
        if error := response_json.get("error"):
            return FetchTemperatureError(
                city_id=city["id"],
                city_name=city["name"],
                code=error["code"],
                message=error["message"],
            )
        return TemperatureCreate(
            city_id=city["id"],
            status="success",
            date_time=response_json["current"]["last_updated"],
            temperature=response_json["current"]["temp_c"],
        )


async def fetch_temperatures_for_all_cities(
    cities: dict[str, int | str],
) -> list[TemperatureCreate | FetchTemperatureError]:
    async with ClientSession() as session:
        results: list[
            TemperatureCreate | FetchTemperatureError
        ] = await gather(
            *[_fetch_temperature(session, city) for city in cities]
        )
    return results

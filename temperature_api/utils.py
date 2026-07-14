from datetime import datetime
from decimal import Decimal
from zoneinfo import ZoneInfo

from httpx import AsyncClient

from city_api.models import City
from conf import settings
from temperature_api.schemas import TemperatureBaseSchema


async def get_weather_in_city(client: AsyncClient, city: City) -> TemperatureBaseSchema:
    url = f"{settings.WEATHERAPI_URL}" f"/current.json"

    response = await client.get(
        url,
        params={
            "key": settings.WEATHERAPI_KEY,
            "q": city.name,
        },
        headers={"Accept": "application/json"},
    )

    temperature = str(response.json()["current"]["temp_c"])
    local_datetime = datetime.strptime(
        response.json()["current"]["last_updated"], "%Y-%m-%d %H:%M"
    )
    local_timezone = response.json()["location"]["tz_id"]

    return TemperatureBaseSchema(
        temperature=temperature,
        date_time=local_datetime,
        time_zone=local_timezone,
        city_id=city.id,
    )

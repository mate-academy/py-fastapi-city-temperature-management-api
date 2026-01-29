from datetime import datetime
from typing import TypeVar

import httpx
from fastapi import HTTPException, status

import app.city.schemas as city_schemas
import app.temperature.schemas as temperature_schemas
from core import settings

T = TypeVar("T", city_schemas.CityCreate, city_schemas.CityUpdate)


class WeatherAPIBase:
    """Base class for interacting with the external weather API."""

    _client = httpx.AsyncClient()

    def __init__(self):
        self.api_key = settings.WEATHERAPI_KEY
        self.base_url = settings.WEATHERAPI_URL
        self.timeout = 5.0

    async def _make_request(self, endpoint: str, params: dict):
        params["key"] = self.api_key
        try:
            response = await self._client.get(
                f"{self.base_url}/{endpoint}", params=params, timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()

        except httpx.HTTPStatusError as e:
            if e.response.status_code == status.HTTP_400_BAD_REQUEST:
                return None
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY, detail="External API error"
            )

        except httpx.RequestError:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Weather service unavailable",
            )


class FindCityService(WeatherAPIBase):
    """Service responsible for refining city names using the external weather API."""

    async def refine_city_name(self, city_data: T) -> T:
        """Refines a city name using the external weather API."""
        results = await self._make_request("search.json", {"q": city_data.name})

        if not results:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"City '{city_data.name}' not found",
            )

        if city_data.additional_info:
            info_lower = city_data.additional_info.lower()
            target = next(
                (res for res in results if res["country"].lower() in info_lower),
                results[0],
            )
        else:
            target = results[0]
        city_data.name = target["name"]

        return city_data


class TemperatureService(WeatherAPIBase):
    """Service responsible for fetching current temperature data for cities."""

    async def get_city_temperature_data(
        self, city: city_schemas.City
    ) -> temperature_schemas.TemperatureCreate | None:
        """Fetches current temperature data for a specific city."""
        data = await self._make_request("current.json", {"q": city.name})

        if data:
            data_object = datetime.strptime(
                data["current"]["last_updated"], "%Y-%m-%d %H:%M"
            )

            return temperature_schemas.TemperatureCreate(
                temperature=float(data["current"]["temp_c"]),
                date_time=data_object,
                city_id=city.id,
            )
        return None

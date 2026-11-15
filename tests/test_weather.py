from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest

from app.services.weather import fetch_city_weather


def _mock_response(payload: dict) -> MagicMock:
    response = MagicMock()
    response.raise_for_status = MagicMock()
    response.json = MagicMock(return_value=payload)
    return response


@pytest.mark.asyncio
async def test_fetch_city_weather_handles_missing_geocode_keys():
    client = AsyncMock(spec=httpx.AsyncClient)
    client.get = AsyncMock(
        return_value=_mock_response({"results": [{"name": "Broken"}]})
    )

    result = await fetch_city_weather(client, city_id=1, city_name="Broken")

    assert result.reading is None
    assert result.error is not None
    assert "Unexpected weather data" in result.error


@pytest.mark.asyncio
async def test_fetch_city_weather_handles_invalid_forecast_time():
    client = AsyncMock(spec=httpx.AsyncClient)
    client.get = AsyncMock(
        side_effect=[
            _mock_response(
                {"results": [{"latitude": 50.45, "longitude": 30.52}]}
            ),
            _mock_response(
                {"current": {"temperature_2m": 5.0, "time": "not-a-datetime"}}
            ),
        ]
    )

    result = await fetch_city_weather(client, city_id=1, city_name="Kyiv")

    assert result.reading is None
    assert result.error is not None
    assert "Unexpected weather data" in result.error

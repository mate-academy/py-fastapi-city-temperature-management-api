from urllib.parse import quote

import httpx

from app.core.config import settings


class TemperatureProviderError(RuntimeError):
    pass


async def fetch_current_temperature(city_name: str, client: httpx.AsyncClient) -> float:
    url = f"{settings.temperature_provider_base_url}/{quote(city_name)}"
    resp = await client.get(url, params={"format": "j1"})
    resp.raise_for_status()

    data = resp.json()
    try:
        value = data["current_condition"][0]["temp_C"]
    except (KeyError, IndexError, TypeError) as exc:
        raise TemperatureProviderError(f"Unexpected response for city '{city_name}'.") from exc

    try:
        return float(value)
    except (TypeError, ValueError) as exc:
        raise TemperatureProviderError(f"Invalid temperature value for city '{city_name}'") from exc

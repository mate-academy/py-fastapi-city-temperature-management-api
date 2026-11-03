import asyncio

import httpx

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"


class WeatherError(Exception):
    pass


async def fetch_temperature(
        client: httpx.AsyncClient,
        city_name: str
) -> float:
    try:
        geo = await client.get(
            GEOCODING_URL,
            params={"name": city_name, "count": 1}
        )
        geo.raise_for_status()
        results = geo.json().get("results")
        if not results:
            raise WeatherError(
                f"City '{city_name}' not found in geocoding service"
            )

        weather = await client.get(
            FORECAST_URL,
            params={
                "latitude": results[0]["latitude"],
                "longitude": results[0]["longitude"],
                "current": "temperature_2m",
            },
        )
        weather.raise_for_status()
        return float(weather.json()["current"]["temperature_2m"])
    except httpx.HTTPError as exc:
        raise WeatherError(
            f"Weather service error for '{city_name}': {exc}"
        ) from exc
    except (KeyError, ValueError) as exc:
        raise WeatherError(f"Unexpected response for '{city_name}'") from exc


async def fetch_all_temperatures(
    cities: list[tuple[int, str]],
) -> tuple[list[tuple[int, float]], list[str]]:
    async with httpx.AsyncClient(timeout=10.0) as client:
        results = await asyncio.gather(
            *(fetch_temperature(client, name) for _, name in cities),
            return_exceptions=True,
        )

    ok: list[tuple[int, float]] = []
    failed: list[str] = []
    for (city_id, name), result in zip(cities, results):
        if isinstance(result, Exception):
            failed.append(name)
        else:
            ok.append((city_id, result))
    return ok, failed

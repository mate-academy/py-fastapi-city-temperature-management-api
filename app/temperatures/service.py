import httpx

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"


async def fetch_temperature(
        client: httpx.AsyncClient,
        city_name: str
) -> float | None:
    """Return current temperature in °C or None if it can't be fetched."""
    try:
        geo = await client.get(
            GEOCODING_URL, params={"name": city_name, "count": 1}
        )
        geo.raise_for_status()
        results = geo.json().get("results")
        if not results:
            return None

        weather = await client.get(
            FORECAST_URL,
            params={
                "latitude": results[0]["latitude"],
                "longitude": results[0]["longitude"],
                "current_weather": "true",
            },
        )
        weather.raise_for_status()
        return weather.json()["current_weather"]["temperature"]
    except (httpx.HTTPError, KeyError):
        return None

import httpx


GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"


async def get_current_temperature(
    client: httpx.AsyncClient,
    city_name: str,
) -> float:
    geocoding_response = await client.get(
        GEOCODING_URL,
        params={
            "name": city_name,
            "count": 1,
            "language": "en",
            "format": "json",
        },
    )
    geocoding_response.raise_for_status()

    geocoding_data = geocoding_response.json()
    results = geocoding_data.get("results")
    print(results, "results 1")

    if not results:
        raise ValueError(f"City not found: {city_name}")

    latitude = results[0]["latitude"]
    longitude = results[0]["longitude"]

    weather_response = await client.get(
        WEATHER_URL,
        params={
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m",
            "timezone": "UTC",
        },
    )
    weather_response.raise_for_status()

    weather_data = weather_response.json()
    current = weather_data.get("current")
    print(current, "current 2")
    if not current:
        raise ValueError(
            f"Temperature data not available for {city_name}"
        )

    temperature = current["temperature_2m"]

    return temperature
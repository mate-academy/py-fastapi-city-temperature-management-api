import httpx


GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"


async def fetch_temperature(
        client: httpx.AsyncClient, city_name: str
) -> float:
    geo_response = await client.get(
        GEOCODING_URL,
        params={"name": city_name, "count": 1},
    )
    geo_response.raise_for_status()
    geo_data = geo_response.json()

    results = geo_data.get("results")
    if not results:
        raise ValueError(f"Coordinates for city '{city_name}' not found")

    location = results[0]
    latitude = location["latitude"]
    longitude = location["longitude"]

    weather_response = await client.get(
        FORECAST_URL,
        params={
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m",
        },
    )
    weather_response.raise_for_status()
    weather_data = weather_response.json()

    return weather_data["current"]["temperature_2m"]

import httpx

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"


class WeatherError(Exception):
    """Raised when a city's temperature cannot be fetched."""


async def geocode(client: httpx.AsyncClient, city_name: str) -> tuple[float, float]:
    response = await client.get(GEOCODING_URL, params={"name": city_name, "count": 1})
    response.raise_for_status()
    data = response.json()

    # if there is no "results" key (or it's empty) -> raise WeatherError
    if "results" not in data or not data["results"]:
        raise WeatherError(f"City not found: {city_name}")

    # return latitude and longitude of data["results"][0]
    result = data["results"][0]
    return result["latitude"], result["longitude"]


async def get_current_temperature(client: httpx.AsyncClient, city_name: str) -> float:
    try:
        latitude, longitude = await geocode(client, city_name)
        response = await client.get(
            FORECAST_URL,
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current": "temperature_2m",
            },
        )
        response.raise_for_status()

        return float(response.json()["current"]["temperature_2m"])
    
    except httpx.HTTPError as exc:
        raise WeatherError(
            f"Weather service request failed for {city_name}: {type(exc).__name__}"
        ) from exc
    
    except (KeyError, TypeError, ValueError) as exc:
        raise WeatherError(f"Unexpected response for {city_name}") from exc

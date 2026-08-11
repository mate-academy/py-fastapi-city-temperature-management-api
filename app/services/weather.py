import httpx


GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"


class WeatherServiceError(Exception):
    pass


async def fetch_current_temperature(city_name: str) -> float:
    if not city_name.strip():
        raise WeatherServiceError("City name cannot be empty")

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
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

            locations = geocoding_response.json().get("results", [])

            if not locations:
                raise WeatherServiceError(
                    f"City '{city_name}' was not found in the weather service"
                )

            location = locations[0]

            weather_response = await client.get(
                FORECAST_URL,
                params={
                    "latitude": location["latitude"],
                    "longitude": location["longitude"],
                    "current": "temperature_2m",
                },
            )
            weather_response.raise_for_status()

            temperature = weather_response.json()["current"]["temperature_2m"]
            return float(temperature)

    except httpx.HTTPError as error:
        raise WeatherServiceError(
            "Weather service is unavailable"
        ) from error
    except (KeyError, TypeError, ValueError) as error:
        raise WeatherServiceError(
            "Weather service returned an invalid response"
        ) from error

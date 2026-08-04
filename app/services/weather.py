from datetime import datetime

import httpx


async def fetch_current_temperature(
    city_name: str,
) -> tuple[datetime, float]:
    async with httpx.AsyncClient(
        timeout=10,
    ) as client:
        geocoding_response = await client.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={
                "name": city_name,
                "count": 1,
                "format": "json",
            },
        )

        geocoding_response.raise_for_status()

        locations = geocoding_response.json().get(
            "results",
            [],
        )

        if not locations:
            raise ValueError(
                f"City {city_name} was not found"
            )

        location = locations[0]

        weather_response = await client.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": location["latitude"],
                "longitude": location["longitude"],
                "current": "temperature_2m",
                "timezone": "UTC",
            },
        )

        weather_response.raise_for_status()

        current_weather = weather_response.json()[
            "current"
        ]

        date_time = datetime.fromisoformat(
            current_weather["time"]
        )

        temperature = float(
            current_weather["temperature_2m"]
        )

        return date_time, temperature
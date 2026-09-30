import httpx


async def get_temperature(city_name: str) -> float:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                "https://geocoding-api.open-meteo.com/v1/search",
                params={
                    "name": city_name,
                    "count": 1,
                    "language": "en",
                    "format": "json",
                },
            )

            response.raise_for_status()
            data = response.json()

            if not data.get("results"):
                raise ValueError(
                    f"City '{city_name}' was not found"
                )

            latitude = data["results"][0]["latitude"]
            longitude = data["results"][0]["longitude"]

            response = await client.get(
                "https://api.open-meteo.com/v1/forecast",
                params={
                    "latitude": latitude,
                    "longitude": longitude,
                    "current": "temperature_2m",
                },
            )

            response.raise_for_status()
            data = response.json()

            current = data.get("current")

            if not current or "temperature_2m" not in current:
                raise ValueError(
                    f"Unexpected forecast response for city '{city_name}'"
                )

            temperature = current["temperature_2m"]

            if not isinstance(temperature, (int, float)):
                raise ValueError(
                    f"Invalid temperature value for city '{city_name}'"
                )

            return float(temperature)

        except httpx.HTTPError as e:
            raise ValueError(
                f"Weather API request failed for city '{city_name}': {e}"
            )

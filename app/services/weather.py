import httpx


class WeatherServiceError(Exception):
    pass


async def fetch_temperature(
        client: httpx.AsyncClient,
        city_name: str
) -> float:
    try:
        response = await client.get(
            f"https://wttr.in/{city_name}",
            params={"format": "j1"},
        )
        response.raise_for_status()
        data = response.json()
        return float(data["current_condition"][0]["temp_C"])

    except (
            httpx.HTTPError,
            KeyError,
            IndexError,
            TypeError,
            ValueError
    ) as exception:
        raise WeatherServiceError(
            f"Could not fetch temperature for {city_name}"
        ) from exception

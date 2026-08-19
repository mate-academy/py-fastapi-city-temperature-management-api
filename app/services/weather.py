import httpx


OPEN_METEO_URL = 'https://api.open-meteo.com/v1/forecast'


async def get_current_temperature(
    latitude: float,
    longitude: float,
) -> tuple[float, str]:
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'current': 'temperature_2m',
        'temperature_unit': 'celsius',
        'timezone': 'auto',
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(
            OPEN_METEO_URL,
            params=params,
            timeout=10.0,
        )

    response.raise_for_status()

    data = response.json()

    temperature = data['current']['temperature_2m']
    date_time = data['current']['time']

    return temperature, date_time

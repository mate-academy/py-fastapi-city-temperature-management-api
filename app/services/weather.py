import httpx

CITY_COORDINATES = {
    "Kyiv": (50.45, 30.52),
    "Dnipro": (48.46, 35.05),
    "Lviv": (49.84, 24.03),
    "Odesa": (46.48, 30.73),
}


async def get_current_temperature(city_name: str) -> float:
    coordinates = CITY_COORDINATES.get(city_name)

    if coordinates is None:
        raise ValueError(f"Coordinates for '{city_name}' not found")

    latitude, longitude = coordinates

    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}"
        f"&longitude={longitude}"
        "&current=temperature_2m"
    )

    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    response.raise_for_status()

    data = response.json()

    return data["current"]["temperature_2m"]

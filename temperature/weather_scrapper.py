import httpx
import asyncio

GEOCODING_BASE_URL = "https://geocoding-api.open-meteo.com/"
GEOCODING_API_URL = "https://api.open-meteo.com/v1/forecast"


async def get_city_coordinates(client: httpx.AsyncClient, city):
    cities_params = {
        "count": 1,
        "name": city
    }

    cities_response = await client.get(f"{GEOCODING_BASE_URL}/v1/search", params=cities_params)
    cities_response.raise_for_status()
    result = cities_response.json()

    if not result.get("results"):
        return None

    latitude = result["results"][0]["latitude"]
    longitude = result["results"][0]["longitude"]

    return { "latitude": latitude, "longitude": longitude }


async def get_weather(client: httpx.AsyncClient, city: str):
    city_coordinates = await get_city_coordinates(client, city)

    if city_coordinates is None:
        return None

    temperature_params = {
        "latitude": city_coordinates["latitude"],
        "longitude": city_coordinates["longitude"],
        "current": "temperature_2m",
    }

    temperature_response = await client.get(GEOCODING_API_URL, params=temperature_params)
    temperature_response.raise_for_status()

    temperature_result = temperature_response.json()

    temperature_time = temperature_result["current"]["time"]
    temperature = temperature_result["current"]["temperature_2m"]
    temperature_unit = temperature_result["current_units"]["temperature_2m"]

    return {
        "city": city,
        "temperature_time": temperature_time,
        "temperature": f"{temperature}{temperature_unit}"
    }


async def scrap_cities_weather():
    сities = ["Berlin", "Hamburg"]

    async with httpx.AsyncClient() as client:
        tasks = [
            get_weather(client, city)
            for city in сities
        ]

        result = await asyncio.gather(*tasks)

    return result


print(asyncio.run(scrap_cities_weather()))
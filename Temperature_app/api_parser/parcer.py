import asyncio
import os

from httpx import AsyncClient
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")


def get_api_url(city_name: str) -> str:
    return "".join([
        "https://api.openweathermap.org/data/2.5/weather",
        f"?q={city_name}&appid={API_KEY}"
    ])


async def get_temperature(
        city_name: str,
        client: AsyncClient = AsyncClient()
) -> dict[str:str]:
    response = await client.get(get_api_url(city_name))

    if response.status_code != 404:
        temperature = round(
            response.json().get("main").get("temp") - 273.15, 2
        )
        return {city_name: temperature}
    return None


async def get_temperature_list(cities: list[str]) -> tuple[dict[str:str]]:
    async with AsyncClient() as client:
        tasks = [
            get_temperature(city_name=city, client=client)
            for city in cities
        ]
        temperature_list = await asyncio.gather(*tasks)
    return temperature_list


if __name__ == '__main__':
    print(get_api_url("Kyiv"))
    city_list = [
        "Bilibino",
        "Kyiv"
    ]
    temperatures = asyncio.run(get_temperature_list(city_list))
    print(temperatures)
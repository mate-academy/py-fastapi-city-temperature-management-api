import os

from dotenv import load_dotenv
from httpx import AsyncClient

load_dotenv()

URL = f"https://api.weatherapi.com/v1/current.json"
API_KEY = os.getenv("API_KEY")


async def get_api_temperature(city: str, client: AsyncClient) -> str:
    print(f"Performing request to Weather API for city {city}.")

    response = await client.get(
        URL, params={"key": API_KEY, "q": city}
    )
    print(f"End of request for {city}")
    data = response.json()

    if data["location"]["name"].lower() != city.lower():
        return "N/A"

    return str(data["current"]['temp_c'])

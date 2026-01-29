import httpx
import asyncio
from core.config import settings

WEATHER_API_URL = "http://api.weatherapi.com/v1/current.json"


async def perform_request(city: str) -> dict:
    """Perform async request to Weather API"""
    key_api = settings.API_WEATHER_KEY
    if key_api is None:
        raise ValueError("API_WEATHER_KEY isn't set!")

    headers = {"key": key_api}
    params = {"q": city}

    async with httpx.AsyncClient() as client:
        response = await client.get(
            WEATHER_API_URL,
            params=params,
            headers=headers
        )
        response.raise_for_status()  # Raise exception for bad status codes
        return response.json()


def parse_response(response: dict) -> float:
    """Extract temperature from API response"""
    temperature = response["current"]["temp_c"]
    return float(temperature)


async def get_temperature(city: str) -> float:
    """Get temperature for a city using Weather API"""
    print(f"Performing request to Weather API for city {city}...")
    response = await perform_request(city)
    temperature = parse_response(response)
    return temperature


async def main():
    """Main async function"""
    try:
        temperature = await get_temperature("London")
        print(f"Temperature in London is {temperature}°C")
    except httpx.HTTPStatusError as e:
        print(f"HTTP error occurred: {e}")
    except KeyError as e:
        print(f"Invalid response format: {e}")
    except ValueError as e:
        print(f"Configuration error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    asyncio.run(main())
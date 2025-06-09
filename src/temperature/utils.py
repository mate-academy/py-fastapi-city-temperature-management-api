import aiohttp

import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
WEATHER_API = os.getenv("WEATHER_API")


async def fetch_temperature(city_name: str):
    url = f"{WEATHER_API}?key={API_KEY}&q={city_name}&aqi=no"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    return f"Error: {response.status}"

                data = await response.json()
                return data["current"]["temp_c"] if "current" in data else None

    except aiohttp.ClientError as e:  # connect error
        return f"Error of connection: {e}"
    except Exception as e:  # other error
        return f"Error: {e}"

import os
import sys
from datetime import datetime

import httpx
from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv("WEATHER_API_KEY")
BASE_URL = "http://api.weatherapi.com/v1/current.json"
LANGUAGE = "en"


async def fetch_weather(city_name: str) -> dict:
    async with httpx.AsyncClient() as client:
        url = f"{BASE_URL}?key={API_KEY}&q={city_name}&lang={LANGUAGE}&units=metric"
        response = await client.get(url)

        if response.status_code == 200:
            data = response.json()
            localtime = data["location"]["localtime"]
            temperature = data["current"]["temp_c"]

            datetime_obj = datetime.strptime(localtime, "%Y-%m-%d %H:%M")

            return {
                "datetime": datetime_obj,
                "temperature": temperature
            }
        else:
            raise ValueError("Failed to fetch weather data. Please try again later.")


async def main():
    if len(sys.argv) < 2:
        print("Usage: python temp_script.py <city_name>")
        sys.exit(1)

    city_name = sys.argv[1]
    weather_data = await fetch_weather(city_name)
    print(f"Weather in {city_name}:")
    print(f"Temperature: {weather_data['temperature']}°C")
    print(f"Local time: {weather_data['datetime']}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

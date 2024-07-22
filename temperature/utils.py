import requests
from dotenv import load_dotenv
import os
import asyncio
load_dotenv()
import aiohttp
WEATHERAPI_KEY = os.getenv("WEATHERAPI_KEY")


async def get_current_temperature(city_name: str) -> float:
    url = f"https://api.weatherapi.com/v1/current.json?key={WEATHERAPI_KEY}&q={city_name}"
    print(url)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            print (response)
            if response.status == 200:
                data = await response.json()
                current_temperature = data["current"]["temp_c"]
                return current_temperature
            else:
                print("Failed to retrieve temperature data")
                return 666
        


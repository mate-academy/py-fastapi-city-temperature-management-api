import httpx

from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")
URL = "http://api.weatherapi.com/v1/current.json"


async def get_weather(city):
    async with (httpx.AsyncClient() as client):
        print(f"Performing request to Weather API for city {city.name}...")
        response = await client.get(URL, params={"key": API_KEY, "q": city.name})
        if response.status_code == 200:
            weather_data = response.json()
            return {
                "city": city.id,
                "time": weather_data['location']['localtime'],
                "temperature": weather_data['current']['temp_c']
            }
        else:
            return None

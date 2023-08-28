import os
from datetime import datetime

from dotenv import load_dotenv

load_dotenv()


WEATHER_API_URL = "http://api.weatherapi.com/v1/current.json"


async def get_city_weather(city_name: str, client):
    city_weather = await client.get(
        url=WEATHER_API_URL,
        params={"key": os.getenv("WEATHER_API_KEY"), "q": city_name}
    )
    city_weather = city_weather.json()["current"]
    return await parse_city_weather(city_weather)


async def parse_city_weather(city_weather: dict):
    time_measured = datetime.strptime(city_weather["last_updated"], "%Y-%m-%d %H:%M")
    temperature = city_weather["temp_c"]
    return time_measured, temperature

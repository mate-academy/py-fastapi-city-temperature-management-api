import json

from temperature import models

import os
from dotenv import load_dotenv
import httpx

from temperature.models import Temperature

load_dotenv()

API_KEY = os.environ.get("API_KEY")
URL = "http://api.weatherapi.com/v1/current.json"


async def get_weather(city) -> Temperature:
    params = {
        "q": city,
        "key": API_KEY,
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(URL, params=params)

    result = json.load(response.content)

    temperature = result["current"]["temp_c"]

    return temperature

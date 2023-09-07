import json
import os
import httpx
from dotenv import load_dotenv
from sqlalchemy import select

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_URL = os.getenv("API_URL")


async def get_temperature(city_name):
    request_values = {
        "q": city_name,
        "key": API_KEY
    }
    print(request_values)
    async with httpx.AsyncClient() as a_client:
        print("--++" * 40)
        print(API_URL)
        result = await a_client.get(API_URL, params=request_values)
        city_temp = json.loads(result.content)["current"]["temp_c"]
        print(city_temp)

    return city_temp





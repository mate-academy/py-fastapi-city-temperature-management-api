import os
from typing import Tuple, Union

import httpx
from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv()

URL = "https://api.weatherapi.com/v1/current.json"
API_KEY = os.environ.get("WEATHER_API_KEY")


async def get_weather(
        location: str,
        url: str = URL,
        api_key: str = API_KEY
) -> Tuple[bool, Union[str, float]]:
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    msg_api = f"You need to visit {domain} and get your API key."
    msg_doc = f"You may visit {domain}/docs/ for more information."

    if not api_key:
        return False, f"No API key provided. {msg_api}"

    params = {"key": api_key, "q": location}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        if response.status_code != 200:
            return False, f"Request error: {response.status_code}. {msg_doc}"

        weather_data = response.json()
        if "error" in weather_data:
            return False, f"API error: {weather_data['error']['message']}"

        temperature = weather_data["current"]["temp_c"]
        return True, temperature

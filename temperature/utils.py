import os

import httpx
from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv()

URL = "https://api.weatherapi.com/v1/current.json"
API_KEY = os.environ.get("WEATHER_API_KEY")


async def get_weather(location: str, url: str = URL, api_key: str = API_KEY) -> tuple:
    """Get weather from API and return the result as a tuple (success, result)."""
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    msg_api = f"You need to visit {domain} and get your API key."
    msg_doc = f"You may visit {domain}/docs/ for more information."

    if not api_key:
        return False, f"No API key provided. {msg_api}"

    params = {"key": api_key, "q": location}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params)
            response.raise_for_status()
            weather_data = response.json()

            if "error" not in weather_data:
                temperature = weather_data["current"]["temp_c"]
                return temperature
            else:
                return f"API error: {weather_data['error']['message']}"

        except httpx.RequestError as e:
            return False, f"Request error: {e}. {msg_doc}"
        except Exception as e:
            return False, f"Unexpected error: {e}. {msg_doc}"

import os
from datetime import datetime

import httpx
import json
from dotenv import load_dotenv

from city.models import City


load_dotenv()

API_KEY = os.getenv("WEATHER_API_KEY")
BASE_URL = os.getenv("WEATHER_API_URL")


async def get_weather(client: httpx.AsyncClient, city: City) -> dict | None:
    try:
        response = await client.get(BASE_URL,
                                    params={"key": API_KEY, "q": city.name})
        response.raise_for_status()
        data = response.json()

        return {
            "city_id": city.id,
            "temperature": data["current"]["temp_c"],
            "date_time": datetime.now()
        }

    except httpx.RequestError as e:
        print(f"Network or HTTP error occurred: {e}")
        return None
    except json.JSONDecodeError:
        print("Error decoding JSON response.")
        return None
    except KeyError as e:
        print(f"Missing expected key in the response: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

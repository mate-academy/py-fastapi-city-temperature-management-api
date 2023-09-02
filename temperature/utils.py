import os
import httpx

from dotenv import load_dotenv

load_dotenv()


async def get_weather(city: str) -> dict:
    api_key = os.environ.get("API_KEY")
    url = (
        f"http://api.weatherapi.com/v1/current."
        f"json?key={api_key}&q={city}&aqi=no"
    )

    async with httpx.AsyncClient() as client:
        response = await client.get(
            url=url,
            params={
                "q": city,
                "key": api_key
            }
        )
        data = response.json()

    current = data.get("current")
    date = current.get("last_updated")
    temperature = current.get("temp_c")

    return {"temperature": temperature, "date": date}

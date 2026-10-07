import logging
import httpx


logging.basicConfig(level=logging.INFO)


async def fetch_weather(city: str):
    try:
        # Step 1: Get coordinates
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}"
        async with httpx.AsyncClient(timeout=10.0) as client:
            geo_response = await client.get(geo_url)
            geo_response.raise_for_status()  # raise if status != 200
            geo_data = geo_response.json()

        if "results" not in geo_data or len(geo_data["results"]) == 0:
            logging.error(f"No results found for {city}")
            return None

        lat = geo_data["results"][0]["latitude"]
        lon = geo_data["results"][0]["longitude"]

        # Step 2: Get weather
        weather_url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}&current_weather=true"
        )
        async with httpx.AsyncClient(timeout=10.0) as client:
            weather_response = await client.get(weather_url)
            weather_response.raise_for_status()
            weather_data = weather_response.json()

        current = weather_data.get("current_weather", {})
        if not current:
            logging.error("No current weather data in response")
            return None

        return {
            "temperature": current.get("temperature"),
        }

    except httpx.HTTPError as e:
        logging.error(f"HTTP error fetching weather: {e}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return None

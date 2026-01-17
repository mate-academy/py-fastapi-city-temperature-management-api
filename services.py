import httpx
from datetime import datetime
import schemas
import asyncio

async def fetch_city_weather(city_name: str) -> float | None:
    async with httpx.AsyncClient() as client:
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language=en&format=json"
        geo_response = await client.get(geo_url)
        geo_data = geo_response.json()

        if not geo_data.get("results"):
            return None

        location = geo_data.get("results")[0]
        lat = location["latitude"]
        lon = location["longitude"]

        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        weather_response = await client.get(weather_url)
        weather_data = weather_response.json()

        current_weather = weather_data.get("current_weather")
        if not current_weather:
            return None

        return current_weather.get("temperature")


async def update_weather_for_all_cities(db, cities, create_temp_func):
    results = []
    # Створюємо словник для зберігання результатів
    temp_results = {}

    async def fetch_and_store(city):
        temp = await fetch_city_weather(city.name)
        temp_results[city.id] = temp

    # Використовуємо сучасний TaskGroup (Python 3.11+)
    async with asyncio.TaskGroup() as tg:
        for city in cities:
            tg.create_task(fetch_and_store(city))

    # Після завершення групи обробляємо зібрані дані
    for city in cities:
        temp = temp_results.get(city.id)
        if temp is not None:
            new_temp_data = schemas.TemperatureCreate(
                city_id=city.id,
                temperature=temp,
                date_time=datetime.now(),
            )
            db_record = await create_temp_func(db, new_temp_data)
            results.append(db_record)

    return results

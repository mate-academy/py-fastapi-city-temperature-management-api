import httpx
import random

# Replace this with real API call if you have an API key
async def fetch_temperature_async(city_name: str) -> float:
    # Fake for now
    await httpx.AsyncClient().get("https://httpbin.org/get")  # simulate I/O
    return round(15 + random.uniform(-5, 10), 2)  # mock temp

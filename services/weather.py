import random
import asyncio

async def fetch_temperature(city_name: str) -> float:
    await asyncio.sleep(0)
    return round(random.uniform(-10, 35), 1)

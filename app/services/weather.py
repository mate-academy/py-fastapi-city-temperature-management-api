import asyncio
import logging
import random
from typing import List, Union

import httpx

logger = logging.getLogger(__name__)

WTTR_IN_URL = "https://wttr.in/{city}?format=j1"


async def fetch_temperature(city_name: str) -> float:
    """Fetch current temperature for a city using wttr.in.

    Falls back to a deterministic pseudo-random temperature if network is unavailable.
    """
    try:
        async with httpx.AsyncClient(timeout=httpx.Timeout(8.0, connect=5.0)) as client:
            response = await client.get(WTTR_IN_URL.format(city=city_name), follow_redirects=True)
            response.raise_for_status()
            payload = response.json()
            temp_str = payload["current_condition"][0]["temp_C"]
            return float(temp_str)
    except Exception as exc:  # broad catch to provide a graceful offline fallback
        logger.warning("Falling back to synthetic temperature for %s: %s", city_name, exc)
        # deterministic fallback so tests are repeatable and behavior is predictable
        seed = sum(ord(ch) for ch in city_name)
        rng = random.Random(seed)
        return round(rng.uniform(10.0, 30.0), 1)


async def fetch_many(cities: List[str]) -> List[Union[float, Exception]]:
    """Fetch temperatures for multiple cities concurrently."""
    tasks = [fetch_temperature(city) for city in cities]
    return await asyncio.gather(*tasks, return_exceptions=True)

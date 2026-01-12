import aiohttp
import asyncio
from typing import List, Dict, Optional
import os
from dotenv import load_dotenv

load_dotenv()


class WeatherService:
    def __init__(self):
        self.api_key = os.getenv("OPENWEATHER_API_KEY", "")
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"

    async def fetch_temperature(self, city_name: str) -> Optional[float]:
        """Fetch current temperature for a city using OpenWeatherMap API"""
        if not self.api_key:
            # Fallback to mock data if no API key is provided
            return await self._get_mock_temperature(city_name)

        params = {
            "q": city_name,
            "appid": self.api_key,
            "units": "metric"
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.base_url, params=params, timeout=10) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("main", {}).get("temp")
                    else:
                        print(f"Error fetching temperature for {city_name}: {response.status}")
                        return await self._get_mock_temperature(city_name)
        except Exception as e:
            print(f"Exception fetching temperature for {city_name}: {e}")
            return await self._get_mock_temperature(city_name)

    async def fetch_temperatures_for_cities(self, cities: List[Dict]) -> List[Dict]:
        """Fetch temperatures for multiple cities concurrently"""
        tasks = []
        for city in cities:
            task = self.fetch_temperature(city["name"])
            tasks.append(task)

        temperatures = await asyncio.gather(*tasks)

        results = []
        for city, temp in zip(cities, temperatures):
            if temp is not None:
                results.append({
                    'city_id': city['id'],
                    'temperature': temp
                })

        return results

    async def _get_mock_temperature(self, city_name: str) -> float:
        """Generate mock temperature for testing"""
        # Simple hash-based temperature generation for consistency
        hash_val = sum(ord(c) for c in city_name)
        return 15 + (hash_val % 20) - 10  # Between 5-25°C


weather_service = WeatherService()

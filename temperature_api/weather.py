import logging

import aiohttp


async def get_current_temperature(city_name: str) -> float:
    api_key = "8b9ce605404927bbf570cca9cdc0cf13"
    base_url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": city_name,
        "appid": api_key,
        "units": "metric"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(base_url, params=params) as response:
            data = await response.json()

            if response.status != 200:
                logging.error(
                    f"Error fetching temperature data for {city_name}: {data}"
                )
                raise ValueError("Error fetching temperature data from the API.")

            if "main" in data and "temp" in data["main"]:
                temperature = data["main"]["temp"]
                return temperature
            else:
                logging.error(f"Invalid API response for {city_name}: {data}")
                raise ValueError(
                    "Invalid API response format or missing temperature data."
                )

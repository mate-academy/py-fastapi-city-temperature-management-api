import aiohttp

async def get_current_temperature(city_name: str) -> float:
    api_key = "a8d0c1f8476bb1f36dfa1dfed4b52ea2"
    base_url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": city_name,
        "appid": api_key,
        "units": "metric"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(base_url, params=params) as response:
            data = await response.json()

            temperature = data["main"]["temp"]
            return temperature


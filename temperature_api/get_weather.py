import httpx

API_KEY = "2e9e0cf4161e4d2587c172158230708"


async def get_temperature_from_weatherapi(city_name):
    base_url = "https://api.weatherapi.com/v1/current.json"
    params = {"key": API_KEY, "q": city_name}

    async with httpx.AsyncClient() as client:
        response = await client.get(base_url, params=params)

        if response.status_code == 200:
            data = response.json()
            temperature_celsius = data["current"]["temp_c"]
            return temperature_celsius
        else:
            response.raise_for_status()

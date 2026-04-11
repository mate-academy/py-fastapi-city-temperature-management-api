import httpx

API_KEY = "YOUR_API_KEY"


async def fetch_temperature(city_name: str) -> float:
    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": city_name,
        "appid": API_KEY,
        "units": "metric",
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)

    data = response.json()

    return data["main"]["temp"]

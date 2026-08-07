import httpx

BASE_URL = "http://api.weatherapi.com/v1"
KEY = "03c945043f1c49c7aad221217262507"

async def get_temp(city: str) -> float:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/current.json",
            params={
                "key": KEY,
                "q": city,
                "aqi": "no",
            },
        )
        response.raise_for_status()

    return response.json()["current"]["temp_c"]
